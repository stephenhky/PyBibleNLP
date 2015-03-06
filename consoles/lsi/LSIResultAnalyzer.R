library(xlsx)

# set LSIResultPrefix
# set Excel.FileName

LSI.WholeBible<-read.csv(paste(LSIResultPrefix, '_WholeBible.csv', sep=''), stringsAsFactors=FALSE)
LSI.OldTestament<-read.csv(paste(LSIResultPrefix, '_OldTestament.csv', sep=''), stringsAsFactors=FALSE)
LSI.NewTestament<-read.csv(paste(LSIResultPrefix, '_NewTestament.csv', sep=''), stringsAsFactors=FALSE)

write.xlsx(LSI.WholeBible, Excel.FileName, sheetName='Whole Bible')
write.xlsx(LSI.OldTestament, Excel.FileName, sheetName='Old Testament', append=TRUE)
write.xlsx(LSI.NewTestament, Excel.FileName, sheetName='New Testament', append=TRUE)
