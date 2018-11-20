import xlsxwriter

def export(events):
    sortedEvents = sorted(events, key=lambda event: (event['projectId'], event['storyNo']))
    currentProjectId = ''
    workBook = xlsxwriter.Workbook('test.xlsx')
    workSheet = None
    row = 1
    for event in sortedEvents:
        if (currentProjectId != event['projectId']):
                currentProjectId = event['projectId']
                workSheet = workBook.add_worksheet(currentProjectId)
                workSheet.write('A1', "StoryNo")
                workSheet.write('B1', "Comment")
                workSheet.write('C1', "Start")
                workSheet.write('D1', 'End')
                workSheet.write('E1', 'Duration')
                row = 1
        
        workSheet.write(row, 0, event['storyNo'])
        workSheet.write(row, 1, event['comment'])
        workSheet.write(row, 2, event['start'])
        workSheet.write(row, 3, event['end'])
        workSheet.write(row, 4, event['duration'])
        row += 1

    workBook.close()