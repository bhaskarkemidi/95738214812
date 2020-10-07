import tkinter as tk
from tkinter import *
from uuid import getnode as get_mac
from PIL import Image
from PIL import ImageTk
from io import BytesIO
import requests
import time
import base64
import blink

# initialization variable's
response_dict = dict()
order_info = dict()
solve = ""
sec = 60
mid = ""
# default decorate
small_text = 'Lato 14'
default_colour, low_def_colour, heading_colour = "#6d0319", "#331D14", "#F4862D"
text_font = "Verdana"
font = 'Lato'
fore_ground = "#ffffff"
upper_ground = "#f29c05"
regular_text = ("Lato", "16")
bold_text = ('Lato', "24", "bold")
heavy_text = ('Lato', "25")


# at boot up checking internet every 5 seconds
def connection():
    try:
        while True:
            if requests.get("https://www.google.com"):
                break
    except requests.ConnectionError:
        time.sleep(5)
        print("not connected")
        connection()
    return


connection()
print("loading page")
time.sleep(1)
try:
    print("In try block:")
    # Get the response from the API endpoint.
    response = requests.get("https://www.idlimachine.com/api/service/products")
    pic = "https://www.idlimachine.com/uploads/panepuripic/15632591095d2d70e5a0529.jpg"
    response1 = requests.get(pic)
    img1 = Image.open(BytesIO(response1.content))
    data = response.json()


    class SampleApp(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
            # the container is where we'll stack a bunch of frames
            # on top of each other, then the one we want visible
            # will be raised above the others
            container = tk.Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            self.frames = {}
            for F in (StartPage, PageOne, PageThree, PageFailed, TimerPage, ThanksOrdering, ConnectionLost):
                page_name = F.__name__
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame
                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame("StartPage")

            # internet checking every 10 second's
            # def check_net():
            #     try:
            #         requests.get("http://www.google.com")
            #         net_status = True
            #     except requests.ConnectionError:
            #         net_status = False
            #     self.after(10000, check_net)  # do checking again ten second's later
            #     if not net_status:
            #         # showinfo("Title", "No Internet Connection")
            #         print("trying to connect")
            #         self.show_frame("ConnectionLost")
            #         frame.tkraise()
            #         self.update()
            #
            # check_net()
        # it call's the page base on page_name
        def show_frame(self, page_name):

            if page_name == 'ConnectionLost':
                def connection_loss():
                    try:
                        if requests.get("https://www.google.com"):
                            self.after_cancel(connecting)
                            frame1 = self.frames['StartPage']
                            frame1.tkraise()
                            self.update()
                            return
                    except requests.ConnectionError:
                        print("not connected")
                        time.sleep(5)
                        connection_loss()
                connecting = self.after(5000, connection_loss)
            if page_name == 'ThanksOrdering':
                global order_info
                frame = self.frames['ThanksOrdering']
                frame.tkraise()
                self.label_2 = Label(frame, text="Oder_Number :- [{}]".format(order_info.get('orderNumber')), font=regular_text, fg=upper_ground, bg=default_colour)
                self.label_2.place(x=350, y=390)
                self.update()
            if page_name == 'PageOne':
                frame = self.frames['PageOne']
                frame.tkraise()
                frame.qr_method()
                frame.update()

                url_status = 'https://www.idlimachine.com/api/service/transactionQRStatus'
                print(response_dict)
                params = dict()
                params['orderId'] = response_dict['orderId']
                # adding sleep for user delay
                time.sleep(10)
                paid = False
                counter = 1
                while not paid:
                    try:
                        print("counter :", counter)
                        if requests.get("https://www.idlimachine.com/contactus"): #https://www.google.com/
                            upload = requests.post(url_status, params)
                            message = upload.json()
                            response2_message = message.get("message")
                            response2_status = message.get("status")
                            print("message:", response2_message, "response :", response2_status)
                            if response2_message == 'success' and response2_status == 1:
                                frame = self.frames['PageThree']
                                frame.tkraise()
                                self.update()
                                order_info['orderNumber'] = message['orderInfo']['orderNumber']
                                #order_info['orderId'] = message['orderId']
                                blink.integrate()
                                params.clear()
                                response_dict.clear()
                                paid = True
                                break
                            if (counter == 18) or (response2_message == 'failure' and response2_status == 2):
                                frame = self.frames['PageFailed']
                                frame.tkraise()
                                self.update()
                                params.clear()
                                response_dict.clear()
                                paid = False
                                break
                    except Exception as ee:
                        print("something went wrong at QR Page %s", ee)
                        frame = self.frames['ConnectionLost']
                        frame.tkraise()
                        self.update()
                        break
                    time.sleep(5)
                    counter += 1
                # after while next statement continues
                if paid:
                    time.sleep(3)
                    frame = self.frames['TimerPage']
                    frame.show_case()
                    frame.tkraise()
                    self.update()
                if not paid:
                    time.sleep(15)
                    frame = self.frames['StartPage']
                    frame.tkraise()
                    print("start_page  called after payment unsuccessful")
                    self.update()
            else:
                frame = self.frames[page_name]
                frame.tkraise()
                self.update()

    class StartPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.pack(fill="both", expand=1)

            self.img = Image.open("images/logo.png")
            self.img.thumbnail((220, 250))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=0, y=0)
            # api image
            img1.thumbnail((350, 500))
            self.photo_single = ImageTk.PhotoImage(img1)
            self.image_single = Label(self.frame, image=self.photo_single, bg=default_colour)
            self.image_single.place(x=40, y=120)

            self.img = Image.open("images/scan_icon.png")
            self.img.thumbnail((50, 50))
            self.photo_upi = ImageTk.PhotoImage(self.img)
            self.upi_label = Label(self, image=self.photo_upi, bg=default_colour)
            self.upi_label.place(x=600, y=90)
            self.img = Image.open("images/pick.png")
            self.img.thumbnail((50, 50))
            self.photo_pick = ImageTk.PhotoImage(self.img)
            self.pick_label = Label(self, image=self.photo_pick, bg=default_colour)
            self.pick_label.place(x=600, y=250)
            self.label_1 = Label(self.frame, text="Pay Using UPI QR", bg=default_colour, fg=fore_ground, font=bold_text)
            self.label_1.place(x=660, y=95)
            self.label1_desc1 = Label(self.frame, text="Scan the QR code on the", bg=default_colour, fg=fore_ground, font=regular_text)
            self.label1_desc1.place(x=610, y=145)
            self.label1_desc2 = Label(self.frame, text="touch screen & complete the", bg=default_colour, fg=fore_ground, font=regular_text)
            self.label1_desc2.place(x=610, y=170)
            self.label1_desc3 = Label(self.frame, text="payment on your app", bg=default_colour, fg=fore_ground, font=regular_text)
            self.label1_desc3.place(x=610, y=196)
            self.label_2 = Label(self.frame, text="Pick", bg=default_colour, fg=fore_ground, font=bold_text)
            self.label_2.place(x=660, y=255)
            self.label2_desc1 = Label(self.frame, text="A plate of Idli is dispensed in out", bg=default_colour, fg=fore_ground, font=regular_text)
            self.label2_desc1.place(x=610, y=300)
            self.label2_desc2 = Label(self.frame, text="the machine in less than 2", bg=default_colour, fg=fore_ground, font=regular_text)
            self.label2_desc2.place(x=610, y=330)
            self.label2_desc3 = Label(self.frame, text="minutes", bg=default_colour, fg=fore_ground, font=regular_text)
            self.label2_desc3.place(x=610, y=358)
            self.frame_footer = Frame(self.frame, bg=upper_ground)
            self.frame_footer.place(x=30, height=60, relwidth=0.92, y=480)
            self.footer_1 = Label(self.frame_footer, text=(data["data"][0]["name"]), bg=upper_ground, font=bold_text, fg=default_colour)
            self.footer_1.place(x=18, y=10)
            self.footer_2 = Label(self.frame_footer, text="Price : ₹" + (data["data"][0]["price"]), bg=upper_ground, font=bold_text, fg=default_colour)
            self.footer_2.place(x=370, y=10)
            self.pay_img = PhotoImage(file="images/Order.gif")
            self.canvas = Canvas(self.frame_footer, bg=default_colour)
            self.canvas.place(x=10, y=100)
            self.footer_3 = Button(self.frame, image=self.pay_img, bg="black", command=lambda: self.validate_qr(), activebackground=upper_ground,
                                   font=heavy_text, fg=default_colour, relief='groove')
            self.footer_3.place(x=730, y=477)

        def validate_qr(self):
            global sec
            sec = 60
            try:
                url2 = 'https://www.idlimachine.com/api/service/generateQR'
                mac = get_mac()
                response_dict['machineId'] = mac
                response_dict['productId'] = data['data'][0]['id']
                response_dict["price"] = data['data'][0]['price']
                # sending json string
                upload = requests.post(url2, response_dict)
                upload_status = upload.json()
                print("order details", upload_status)
                response_dict['orderId'] = upload_status['orderId']
                order_info['orderId'] = upload_status['orderId']
                image_data = upload_status.get('qr')
                access_data = base64.b64decode(image_data)
                self.img = Image.open(BytesIO(access_data))
                self.img.save('images/qr.png')
                self.controller.show_frame('PageOne')
                return
            except Exception as e:
                print("connection lost at order button %s", e)
                self.controller.show_frame('ConnectionLost')
                return

    class PageOne(tk.Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.place(relwidth=1, relheight=1)

            self.img = Image.open("images/logo.png")
            self.img.thumbnail((220, 250))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=0, y=0)
            self.label_pay = Label(self.frame, text="Pay with QR code", font=bold_text, bg=default_colour, fg=upper_ground)
            self.label_pay.place(x=400, y=40)
            self.timer = Label(self.frame, text="Make payment with-in 90 second's", font=bold_text, bg=default_colour, fg=upper_ground)
            self.timer.place(x=250, y=450)

        def qr_method(self):
            self.qr_image = PhotoImage(file='images/qr.png')
            self.image = Label(self.frame, image=self.qr_image)
            self.image.place(x=380, y=120)
            self.update()

    class PageThree(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.pack(fill="both", expand=1)

            self.tnx_label = Label(self, text="Thank You", font=bold_text, bg=default_colour, fg="white")
            self.tnx_label.place(x=410, y=50)
            self.stuff_label = Label(self, text="Payment Successful", font=bold_text, bg=default_colour, fg="white")
            self.stuff_label.place(x=360, y=100)
            self.img = Image.open("images/green.png")
            self.img.thumbnail((250, 250))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=360, y=160)
            self.stuff_label = Label(self, text="Support :", font=bold_text, bg=default_colour, fg="white")
            self.stuff_label.place(x=430, y=440)
            self.stuff_label = Label(self, text="93987 84580 ", font=bold_text, bg=default_colour, fg="white")
            self.stuff_label.place(x=390, y=480)

    class PageFailed(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.pack(fill="both", expand=1)

            self.stuff_label = Label(self, text="Payment Unsuccessful", font=bold_text, bg=default_colour, fg=fore_ground)
            self.stuff_label.place(x=100, y=100)
            self.img = Image.open("images/unsuccessful.png")
            self.img.thumbnail((250, 250))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=140, y=180)
            self.stuff_label_1 = Label(self, text="In case, any amount is deducted from your bank account,", font=bold_text, bg=default_colour, fg=fore_ground)
            self.stuff_label_1.place(x=100, y=380)
            self.stuff_label_2 = Label(self, text="will be refunded by us with-in in 3-5 working days", font=bold_text, bg=default_colour, fg=fore_ground)
            self.stuff_label_2.place(x=100, y=420)

    class ConnectionLost(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.pack(fill="both", expand=1)

            self.img = Image.open("images/connection-lost.png")
            self.img.thumbnail((900, 1000))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=100, y=50)

    class TimerPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.parent = parent
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.place(relwidth=1, relheight=1)

            self.img = Image.open("images/logo.png")
            self.img.thumbnail((250, 250))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=0, y=0)
            self.select_label = Label(self.frame, text="A plate of Hot idli is getting ready in", bg=default_colour, font=bold_text, fg=upper_ground)
            self.select_label.place(x=200, y=130)
            self.select_label_2 = Label(self.frame, bg=default_colour, font=bold_text, fg=upper_ground)
            self.select_label_2.place(x=200, y=180)
            self.img1 = Image.open("images/singleidli.png")
            self.img1.thumbnail((350, 350))
            self.photo_select_1 = ImageTk.PhotoImage(self.img1)
            self.select_label_1 = Label(self.frame, image=self.photo_select_1, bg=default_colour)
            self.select_label_1.place(x=300, y=300)

        def show_case(self):
            def tick():
                global sec, solve
                sec -= 1
                if sec == 1:
                    print("please wait displayed")
                    self.select_label_2['text'] = "please wait...."
                elif sec < 0:
                    self.select_label_2['text'] = "please wait1...."
                    self.select_label_2.after_cancel(solve)
                    order_info1 = dict()
                    order_info1['orderId'] = order_info['orderId']
                    blink.integrate3()
                    image_url = "https://www.idlimachine.com/api/service/idlimachinepic"
                    image_dict = {'image': open('images/single.png', 'rb')}
                    image_upload = requests.post(url=image_url, files=image_dict, data=order_info1)
                    self.controller.show_frame("ThanksOrdering")
                    print("thanks page called")
                    time.sleep(5)
                    print("startPage called")
                    self.controller.show_frame('StartPage')
                    order_info1.clear()
                    return
                else:
                    self.select_label_2['text'] = str(sec) + "  Seconds..."
                # calling the tick method every 1 second in timer_page
                solve = self.select_label_2.after(1000, tick)
                # Take advantage of the after method of the Label
            tick()

    class ThanksOrdering(tk.Frame):
        def __init__(self, parent, controller):
            Frame.__init__(self, parent)
            self.controller = controller
            self.frame = Frame(self, bg=default_colour)
            self.frame.pack(fill="both", expand=1)
            self.img = Image.open("images/logo.png")
            self.img.thumbnail((350, 350))
            self.photo_select = ImageTk.PhotoImage(self.img)
            self.select_label = Label(self.frame, image=self.photo_select, bg=default_colour)
            self.select_label.place(x=300, y=0)
            self.label = Label(self.frame, text="Thanks for ordering", font=bold_text, fg=upper_ground, bg=default_colour)
            self.label.place(x=340, y=210)
            self.label_4 = Label(self.frame, text="enjoy your idli..!", font=bold_text, fg=upper_ground, bg=default_colour)
            self.label_4.place(x=355, y=248)
            self.label_3 = Label(self.frame, text="if you have any queries, please visit :\n www.idlimachine.com", fg=upper_ground, bg=default_colour, font=regular_text)
            self.label_3.place(x=620, y=535)


    if __name__ == "__main__":
        app = SampleApp()
        # app.attributes('-fullscreen', True)
        app.config(cursor="arrow")
        app.configure(background=default_colour)
        app.geometry("1024x600")
        app.grid_rowconfigure(0, weight=1)
        app.grid_columnconfigure(0, weight=1)
        app.mainloop()

except requests.exceptions.ConnectionError as e:
    time.sleep(5)
    connection()

    app = tk.Tk()
    label = tk.Label(app, text="Internet Error!!!, %s".format(e), foreground="red", font=regular_text)
    label.pack()
    app.config(cursor="arrow")
    app.config(bg='blue')
    app.geometry("1024x600")
    app.mainloop()
