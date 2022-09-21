#include <stdio.h>
#include <intrin.h>
#include <windows.h>
#include <winternl.h>

#define WANTED 0xBC553B82

unsigned int calculate(PCSTR name)
{
	unsigned int crc = -1;
	
	while(*name){
		crc = _mm_crc32_u8(crc, *name);
		name++;
	}
	return crc;
}

void scan_names(PVOID addr)
{
	PIMAGE_DOS_HEADER pDosHeader = (PIMAGE_DOS_HEADER)addr;
	PIMAGE_NT_HEADERS pNtHeader = (PIMAGE_NT_HEADERS)((PBYTE)addr + pDosHeader->e_lfanew);
	PIMAGE_OPTIONAL_HEADER pOptionalHeader = (PIMAGE_OPTIONAL_HEADER)&(pNtHeader->OptionalHeader);
	PIMAGE_EXPORT_DIRECTORY pExportDirectory = (PIMAGE_EXPORT_DIRECTORY)((PBYTE)addr + pOptionalHeader->DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
	PULONG pAddressOfFunctions = (PULONG)((PBYTE)addr + pExportDirectory->AddressOfFunctions);
	PULONG pAddressOfNames = (PULONG)((PBYTE)addr + pExportDirectory->AddressOfNames);
	PUSHORT pAddressOfNameOrdinals = (PUSHORT)((PBYTE)addr + pExportDirectory->AddressOfNameOrdinals);
	
	for (int i = 0; i<pExportDirectory->NumberOfNames; i++) {
		PCSTR name = (PCSTR)((PBYTE)addr + pAddressOfNames[i]);
		unsigned int calc = calculate(name);
		if (calc == WANTED)
			printf("!!! crc32(%s) == 0x%X\n", name, calc);
	}
}

int main(void)
{
	PPEB pPEB = 0;
	PLDR_DATA_TABLE_ENTRY pLDTE = NULL;
	
	pPEB = (PPEB)__readgsqword(0x60);

	printf("PEB: 0x%x\n", (unsigned int)pPEB);
	PLIST_ENTRY pLE = &(pPEB->Ldr->InMemoryOrderModuleList);
	for (
			PLIST_ENTRY pL = pLE->Flink;
			pL != pLE;
			pL = pL->Flink) {
		pL = pL - 1;
		pLDTE = (PLDR_DATA_TABLE_ENTRY)pL;
		
		char dll_path[512], *dll_name;
		wcstombs(dll_path, pLDTE->FullDllName.Buffer, 512);
		dll_name = strrchr(dll_path, '\\');
		dll_name++;
		if (strcmp(dll_name, "KERNEL32.DLL") == 0) {
			printf("%s: 0x%x\n", dll_name, (unsigned int)pLDTE->DllBase);
			scan_names(pLDTE->DllBase);
		}
		pL = pL + 1;
	}
	
	return 0;
}

