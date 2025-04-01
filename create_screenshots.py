from PIL import Image, ImageDraw, ImageFont
import os

def create_screenshot(filename, title):
    # Create a new image with a white background
    img = Image.new('RGB', (800, 600), color='white')
    
    # Create a drawing context
    d = ImageDraw.Draw(img)
    
    # Load a font
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_text = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # Draw title
    d.text((50, 50), title, fill=(0,0,0), font=font_title)
    
    # Draw some mock UI elements
    d.rectangle([50, 150, 750, 250], outline=(200,200,200), width=2)
    d.text((100, 170), "Face Recognition Attendance System", fill=(0,0,0), font=font_text)
    
    # Draw buttons
    d.rectangle([100, 300, 300, 370], fill=(100,150,255), outline=(0,0,0))
    d.text((130, 310), "Login", fill=(255,255,255), font=font_text)
    
    d.rectangle([400, 300, 600, 370], fill=(50,200,100), outline=(0,0,0))
    d.text((430, 310), "Register", fill=(255,255,255), font=font_text)
    
    # Save the image
    img.save(os.path.join('screenshots', filename))

# Create screenshots
os.makedirs('screenshots', exist_ok=True)
create_screenshot('login_screen.png', 'Login Screen')
create_screenshot('register_screen.png', 'Registration Screen')
create_screenshot('attendance_screen.png', 'Attendance Tracking')
