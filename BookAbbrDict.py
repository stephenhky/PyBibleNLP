__author__ = 'hok1'

otbookdict = {
		"ge": "Genesis",
		"ex": "Exodus",
		"le": "Leviticus",
		"nu": "Numbers",
		"de": "Deuteronomy",
		"jos": "Joshua",
		"jdg": "Judges",
		"ru": "Ruth",
		"1sa": "1 Samuel",
		"2sa": "2 Samuel",
		"1ki": "1 Kings",
		"2ki": "2 Kings",
		"1ch": "1 Chronicles",
		"2ch": "2 Chronicles",
		"ezr": "Ezra",
		"ne": "Nehemiah",
		"est": "Esther",
		"job": "Job",
		"ps": "Psalms",
		"pr": "Proverbs",
		"ec": "Ecclesiastes",
		"so": "Song of Songs",
		"is": "Isaiah",
		"je": "Jeremiah",
		"la": "Lamentations",
		"eze": "Ezekiel",
		"da": "Daniel",
		"ho": "Hosea",
		"joe": "Joel",
		"am": "Amos",
		"ob": "Obadiah",
		"jon": "Jonah",
		"mic": "Micah",
		"na": "Nahum",
		"hab": "Habakkuk",
		"zep": "Zephaniah",
		"hag": "Haggai",
		"zec": "Zechariah",
		"mal": "Malachi"
}

ntbookdict = {
		"mt": "Matthew",
		"mk": "Mark",
		"lk": "Luke",
		"jn": "John",
		"ac": "Acts",
		"ro": "Romans",
		"1co": "1 Corinthians",
		"2co": "2 Corinthians",
		"ga": "Galatians",
		"eph": "Ephesians",
		"php": "Philippians",
		"col": "Colossians",
		"1th": "1 Thessalonians",
		"2th": "2 Thessalonians",
		"1ti": "1 Timothy",
		"2ti": "2 Timothy",
		"ti": "Titus",
		"phm": "Philemon",
		"heb": "Hebrews",
		"jam": "James",
		"1pe": "1 Peter",
		"2pe": "2 Peter",
		"1jn": "1 John",
		"2jn": "2 John",
		"3jn": "3 John",
		"jud": "Jude",
		"rev": "Revelation"
}

def getBookName(key):
    if otbookdict.has_key(key):
        return otbookdict[key]
    else:
        return ntbookdict[key]