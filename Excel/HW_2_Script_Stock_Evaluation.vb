Sub stockEvaluation()

On Error Resume Next
Dim ws As Worksheet

' Stock Volume Variables
Dim LastRow As Long
Dim TickerVolumeSV As Double
Dim CurrentTickerSV As String
Dim NextTickerSV As String
Dim totalSV_i As Long

' Yearly Change Variables
Dim CurrentTickerYC As String
Dim PreviousTickerYC As String
Dim NextTickerYC As String
Dim totalYC As Double
Dim totalPctYC As Double
Dim openValueYC As Double
Dim closeValueYC As Double
Dim yearlyChange_i as Long
Dim resultsSV_i As Integer
Dim resultsYC_i As Integer

' Greatest And Smallest Value Variables
Dim LastRowYC As Long
Dim grYC As Double
Dim smYC As Double
Dim grSV As Double
Dim grYCTicker As String
Dim smYCTicker As String
Dim grSVTicker As String
Dim currentGrYC As Double
Dim currentSmYC As Double
Dim currentGrSV As Double
Dim grYC_i As Long

' Loop Worksheets
For Each ws In ActiveWorkbook.Worksheets

    ' Write Headers
    With ws
        .Cells(1, 9).Value = "Ticker"
        .Cells(1, 10).Value = "Yearly Change"
        .Cells(1, 11).Value = "Percent Change"
        .Cells(1, 12).Value = "Total Stock Volume"
        .Cells(2, 14).Value = "Greatest % Increase"
        .Cells(3, 14).Value = "Greatest % Decrease"
        .Cells(4, 14).Value = "Greatest Total Volume"
        .Cells(1, 15).Value = "Ticker"
        .Cells(1, 16).Value = "Value"
    End With
    LastRow = ws.Cells(Rows.Count, 1).End(xlUp).Row
    resultsSV_i = 2

    ' Calculate And Write Total Stock Volume And Yearly Change
    For totalSV_i = 2 To LastRow
        CurrentTickerSV = ws.Cells(totalSV_i, 1).Value
        NextTickerSV = ws.Cells(totalSV_i + 1, 1).Value
        TickerVolumeSV = TickerVolumeSV + ws.Cells(totalSV_i, 7).Value
    
        ' Change To Next Ticker And Write Information Of Current
        If CurrentTickerSV <> NextTickerSV Then
            ws.Cells(resultsSV_i, 9).Value = CurrentTickerSV
            ws.Cells(resultsSV_i, 12).Value = TickerVolumeSV
            resultsSV_i = resultsSV_i + 1
            CurrentTickerSV = Empty
            TickerVolumeSV = Empty            
        End If
    Next  
    resultsYC_i = 2

    ' Calculate Yearly Difference
    For yearlyChange_i = 2 To LastRow
        CurrentTickerYC = ws.Cells(yearlyChange_i, 1).Value
        PreviousTickerYC = ws.Cells(yearlyChange_i - 1, 1).Value
        NextTickerYC = ws.Cells(yearlyChange_i + 1, 1).Value

        ' Detect First Observation For The Stock And Save Opening Value
        If CurrentTickerYC <> PreviousTickerYC Then
            openValueYC = ws.Cells(yearlyChange_i,3)
        End If

        ' Detect Last Observation For The Stock, Calculate Changes And Write Results
        If CurrentTickerYC <> NextTickerYC Then
            closeValueYC = ws.Cells(yearlyChange_i,6)
            totalYC = closeValueYC - openValueYC
            totalPctYC = totalYC / openValueYC
            ws.Cells(resultsYC_i, 10).Value = totalYC
            ws.Cells(resultsYC_i, 11).Value = FormatPercent(totalPctYC)
            If totalYC > 0 Then
                ws.Cells(resultsYC_i, 10).Interior.ColorIndex = 4
            Else
                ws.Cells(resultsYC_i, 10).Interior.ColorIndex = 3
            End If
            resultsYC_i = resultsYC_i + 1
            totalYC = Empty
            totalPctYC = Empty            
        End If
    Next
    LastRowYC = ws.Cells(Rows.Count, 7).End(xlUp).Row
    grSV = 0
    grYC = 0
    smYC = 0

    ' Calculate Greatest and Smallest Values
    For grYC_i = 2 To LastRowYC
        currentGrYC = ws.Cells(grYC_i, 11).Value
        currentSmYC = ws.Cells(grYC_i, 11).Value
        currentGrSV = ws.Cells(grYC_i, 12).Value
        If currentGrYC > grYC Then
            grYC = currentGrYC
            grYCTicker = ws.Cells(grYC_i, 9).Value
        ElseIf currentSmYC < smYC Then
            smYC = currentSmYC
            smYCTicker = ws.Cells(grYC_i, 9).Value
        ElseIf currentGrSV > grSV Then
            grSV = currentGrSV
            grSVTicker = ws.Cells(grYC_i, 9).Value
        End If
    Next
    
    with ws
        .Range("O2").Value = grYCTicker
        .Range("P2").Value = FormatPercent(grYC)
        .Range("O3").Value = smYCTicker
        .Range("P3").Value = FormatPercent(smYC)
        .Range("O4").Value = grSVTicker
        .Range("P4").Value = grSV
    End With

    ws.Columns("I:P").AutoFit
Next

End Sub
