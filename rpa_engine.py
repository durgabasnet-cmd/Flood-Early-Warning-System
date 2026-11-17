from reportlab.pdfgen import canvas
import datetime
import os

def trigger_emergency_rpa(hazard_class, water_level, prob):
    # Generate structured PDF dossier without external APIs
    pdf_filename = f"flood_advisory_class_{hazard_class}.pdf"
    c = canvas.Canvas(pdf_filename)
    c.drawString(100, 750, f"CRITICAL FLOOD ADVISORY - LEVEL {hazard_class}")
    c.drawString(100, 730, f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 710, f"Current Water Level: {water_level:.2f} cm")
    c.drawString(100, 690, f"Flood Probability: {prob:.2f}%")
    c.drawString(100, 650, "Immediate action is required. Please follow municipal guidelines.")
    c.save()
    
    # Mock SMS output to console
    print(f"[RPA MOCK SMS] ALERT! Flood Risk Level {hazard_class} detected.")
    
    return pdf_filename
