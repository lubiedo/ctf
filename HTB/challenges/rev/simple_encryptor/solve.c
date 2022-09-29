#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <time.h>
#include <sys/mman.h>

int main(void)
{
  char *enc, *dec;
  int fd;

  fd = open("./flag.enc", O_RDONLY); /* flawfinder: ignore */
  enc = (char *)mmap(NULL, 32, PROT_READ, MAP_FILE | MAP_SHARED, fd, 0);
  close(fd);

  dec = (char *)malloc(28);

  time_t t;
  memcpy(&t, enc, 4);
  unsigned char *data = (unsigned char *)enc+4; // skip epoch

  srand(t); /* flawfinder: ignore */
  printf("epoch: 0x%04lx (%ld)\n", t, t);
  for (short int j=0; j<28;j++) {
    unsigned int c = data[j];
    unsigned int r = rand(), rr = rand();
    __asm__(
        "mov %1, %%ecx\n\t"
        "mov %0, %%eax\n\t"
        "rorb %%cl, %%al\n\t"
        "mov %%eax, %0"
        : "+r" (c)
        : "r" (rr & 7));
    c ^= r;
    c &= 0xff;

    dec[j] = c;
  }

  printf("%s\n", dec);

  free(dec);
  munmap(enc, 32);
  return 0;
}
