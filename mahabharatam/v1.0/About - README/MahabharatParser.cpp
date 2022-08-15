// MTP.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <fstream>
#include <sstream>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <codecvt>
#include "MTP.h"

void formHtmlfiles(std::wstring csvfilename, std::wstring htmlfilename);

int main()
{
	for (int parva = 1; parva < 19; ++parva)
	{
		char fmtParvaStr[3];
		sprintf_s(fmtParvaStr, "%02d", parva);
		std::string parvaStr = "C:/Users/satis/OneDrive/Personal_Projects/WIP/CPP/input/MBh" + std::string(fmtParvaStr) + ".txt";
		std::wifstream inputFile(std::string(parvaStr).c_str());
		std::locale loc(std::locale::classic(), new std::codecvt_utf8<wchar_t>);
		inputFile.imbue(loc);
		std::cout << parvaStr << "filename";
		std::wstring line;
		std::multimap<std::wstring, std::wstring> verseIdsToSlokaMultimap;
		std::multimap<std::wstring, std::wstring> chapterIdToVerseIdsMultiMap;
		std::set<std::wstring> chapters;;

		int lineno = 0;
		if (inputFile.is_open())
		{
			while (std::getline(inputFile, line)) {
				if (line.substr(0, 1).c_str()[0] == '%')
					continue;
				size_t pos = line.find(' ', 0);
				if (pos == std::wstring::npos)
				{
					std::cout << "no key in lineno" << lineno << std::endl;
				}
				std::wstring keystr = line.substr(0, pos);
				if (isalpha(keystr.back()))
					keystr.pop_back();
				std::wstring valstr = line.substr(pos + 1, std::wstring::npos);
				verseIdsToSlokaMultimap.insert(std::pair<std::wstring, std::wstring>(keystr, valstr));

				std::wstring chapterId = keystr.substr(2, 3);
				chapterIdToVerseIdsMultiMap.insert(std::pair<std::wstring, std::wstring>(chapterId, keystr));

				if (chapters.find(chapterId) == chapters.end())
					chapters.insert(chapterId);

			}
		}
		inputFile.close();

		std::set<std::wstring> verseKeys;         //set to store the unique keys

		wchar_t singlePipe = L'\u0964';
		wchar_t doublePipe = L'\u0965';
		wchar_t delimiter = L',';
		std::wstring headerOfFile = L"Verse";


		for (auto chapterIterator = chapters.begin(); chapterIterator != chapters.end(); chapterIterator++)
		{
			std::wstring chapterId = *chapterIterator;
			auto chapterIdToVerseIdsMultiMapIterator = chapterIdToVerseIdsMultiMap.equal_range(chapterId);
			std::wstring filename;
			std::wstringstream filenameAsStream;
			filenameAsStream << L"C:/temp/output/" << fmtParvaStr << L"/MBh" << fmtParvaStr << L"-" << chapterId;
			filename = filenameAsStream.str();
			std::wstring csvfilename = filename + L".csv";
			std::wofstream formattedFileA(csvfilename, std::ios::out | std::ios::ate);
			std::locale locO(std::locale::classic(), new std::codecvt_utf8<wchar_t>);
			formattedFileA.imbue(locO);

			formattedFileA << headerOfFile << std::endl;
			std::set<std::wstring> alreadyProcessedVerseIds;
			for (auto chapterIdToVerseIdsMultiMapIteratorPair = chapterIdToVerseIdsMultiMapIterator.first; chapterIdToVerseIdsMultiMapIteratorPair != chapterIdToVerseIdsMultiMapIterator.second; ++chapterIdToVerseIdsMultiMapIteratorPair) {

				std::wstring currentVerseId = chapterIdToVerseIdsMultiMapIteratorPair->second;
				if (checkIfCurrentVerseIdIsAlreadyProcessed(alreadyProcessedVerseIds, currentVerseId))
				{
					alreadyProcessedVerseIds.insert(currentVerseId);
					//formattedFileA  <<  chapterIdToVerseIdsMultiMapIteratorPair->second << delimiter;
					auto its = verseIdsToSlokaMultimap.equal_range(chapterIdToVerseIdsMultiMapIteratorPair->second);
					std::wstring verseStr;
					for (auto itr = its.first; itr != its.second; itr++) {
						verseStr += itr->second + singlePipe + L" <br>";
					}
					formattedFileA << verseStr.substr(0, verseStr.length() - 6);
					std::wstring verseIdFormatted = (chapterIdToVerseIdsMultiMapIteratorPair->second).substr(0, 2) + \
						L"-" + (chapterIdToVerseIdsMultiMapIteratorPair->second).substr(2, 3) + L"-" + \
						(chapterIdToVerseIdsMultiMapIteratorPair->second).substr(5, std::wstring::npos);
					formattedFileA << L"   " << doublePipe << verseIdFormatted << doublePipe;
					formattedFileA << std::endl;
				}

			}
			formattedFileA.close();

			formHtmlfiles(csvfilename, filename + L".html");
		}
		// std::cout << " count of keys " << verseKeys.size()  << " count of lines" << verseIdsToSlokaMultimap.size() << std::endl;
	}
}

void formHtmlfiles(std::wstring csvfilename, std::wstring htmlfilename)
{
	std::wstring prefix = L"<tr><td>";
	std::wstring postfix = L"</td></tr>";
	std::wstring headerline = L"<tr><td>verse</td></tr>";

	std::wstring line;
	std::wifstream csvStream(csvfilename);
	std::wofstream htmlStream(htmlfilename, std::ios::ate);
	//std::cout << L"htmlfilename is " << htmlfilename << std::endl;
	htmlStream << "<table border = \"1\">";
	bool init = false;
	if (csvStream.is_open())
	{
		while (getline(csvStream, line))
		{
			if (init == false)
			htmlStream << prefix << line << postfix << std::endl;
		}
	}
	htmlStream << L"</table>";
	csvStream.close();
	htmlStream.close();
}

bool checkIfCurrentVerseIdIsAlreadyProcessed(std::set<std::wstring>& alreadyProcessedVerseIds, std::wstring& currentVerseId)
{
	return alreadyProcessedVerseIds.find(currentVerseId) == alreadyProcessedVerseIds.end();
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
