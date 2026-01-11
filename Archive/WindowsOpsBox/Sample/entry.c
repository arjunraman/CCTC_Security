#include <windows.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
	char key[20];
	printf("Enter key: ");
	fgets(key,20,stdin);
	strtok(key, "\n");
	if (strcmp(key, "123@magicKey") == 0)
	{
		printf("Success!");
	}
	else
	{
		printf("Invalid key.");
	}
	Sleep(5000);
	return 0;
}
