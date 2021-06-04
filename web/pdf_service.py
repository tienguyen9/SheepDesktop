from fpdf import FPDF
from.db_helper_functions import calculateDeadSheep, calculateSheepData, calculatePredatorData
from datetime import date

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 25)
        self.cell(0,10,'Sheep Report', ln=True, align='C')
        self.ln(20)


def generatePDF(reports):

    pdf = PDF('P', 'mm')
    pdf.add_page()
    pdf.set_font('helvetica', '', 8)
    pdf.set_auto_page_break(auto=True, margin=15)
    for report in reports:
        tripID = report.trip.trip_id
        totalSheep, totalLambs, totalExpectedLambs = calculateSheepData(tripID)
        deadSheep = calculateDeadSheep(tripID)
        totalWolves, totalLynx, totalWolverines = calculatePredatorData(tripID)


        pdf.cell(len("TripID")*2, 6, "TripID", border=True)
        pdf.cell(len("Date and time")*3, 6, "Date and time", border=True)
        pdf.cell(len("Spotted sheep")*2, 6, "Spotted sheep", border=True)
        pdf.cell(len("Spotted lambs")*2, 6, "Spotted lambs", border=True)
        pdf.cell(len("Expected lambs")*2, 6, "Expected lambs", border=True)
        pdf.cell(len("Dead animals")*2, 6, "Dead animals", border=True, ln=True)

        pdf.cell(len("TripID")*2, 6, str(tripID), border=True)
        pdf.cell(len("Date and time")*3, 6, str(report.trip.trip_date_time), border=True)
        pdf.cell(len("Spotted sheep")*2, 6, str(totalSheep), border=True)
        pdf.cell(len("Spotted lambs")*2, 6, str(totalLambs), border=True)
        pdf.cell(len("Expected lambs")*2, 6, str(totalExpectedLambs), border=True)
        pdf.cell(len("Dead animals")*2, 6, str(deadSheep), border=True, ln=True)

        pdf.cell(len("Spotted lynx")*2, 6, "Spotted lynx", border=True)
        pdf.cell(len("Spotted wolf")*2, 6, "Spotted wolves", border=True)
        pdf.cell(len("Spotted wolverine")*2, 6, "Spotted wolverines", border=True, ln=True)


        pdf.cell(len("Spotted lynx")*2, 6, str(totalLynx), border=True)
        pdf.cell(len("Spotted wolf")*2, 6, str(totalWolves), border=True)
        pdf.cell(len("Spotted wolverine")*2, 6, str(totalWolverines), border=True, ln=True)
        pdf.cell(18, 6, "Description:", border=True, ln=True)
        pdf.multi_cell(0,10, report.description,1,0, ln=True)
        pdf.cell(18, 6, "", border=False, ln=True)
        pdf.cell(18, 6, "", border=False, ln=True)
        pdf.cell(18, 6, "", border=False, ln=True)
        pdf.cell(18, 6, "", border=False, ln=True)
    

    today = date.today()
    today_format = today.strftime("%b-%d-%Y")

    pdf.output('reports/sheep_report_' + today_format + '.pdf')

