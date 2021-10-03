
import tkinter
from tkinter import *
import PIL
from PIL import Image, ImageTk
import tensorflow as tf
import cv2
import numpy as np

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# add widgets here
class Widget():
    def __init__(self):
        self.cell = ""
        self.window = Tk()
        self._setup_main_window()
    def run(self):
        self.window.mainloop()


    def runModel(self,filename):
        model = tf.keras.models.load_model('covidModel.h5',  compile=False)
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resized_img = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)/255.
        image = np.expand_dims(resized_img, axis = 0)
        predicted = model.predict(image)
        fig = plt.figure(figsize = (18,15))
        plt.imshow(x_test[i][...,0], cmap = 'bone')
        plt.imshow(predicted[i][...,0],alpha = 0.5,cmap = "nipy_spectral")
        plt.savefig("segmentedImage.jpg")


    def _on_add_pressed(self,msg):
        self.entry.delete(0, END)
        self.add_original_image(msg)
        self._insert_message("I am processing your image", "Doctor")
        # self.runModel(msg)
        self.add_segmented_image()

    def _on_enter_pressed(self, event):
        msg = self.entry.get()
        self._insert_message(msg, "You")


        # data = '{"message": "' + msg + '"}'
        # response = requests.post('http://deeplearning-hub.com:8880/webhooks/rest/webhook', data=data)
        # out = json.loads(response.content)
        if msg.lower() == "hello":
            out = "Hello, I am doctor chatbot, I am here to help.\nPlease upload your image above."
            self._insert_message(out,"Doctor")
            # self.entry.place(relwidth=0.98, relheight=0.06, rely=0.008, relx=0.011)
            # self.add.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        if msg.lower() == "goodbye":
            out2 = "Goodbye, it was nice to have you around."
            self._insert_message(out2,"Doctor")
        if (".jpg" in msg) or (".png" in msg):
            self._insert_message("Got it! Processing...", "Doctor")
            self._insert_message("Here is the image you gave me: ","Doctor")
            self._on_add_pressed(msg)

        # for i in out:
        #     try:
        #         out = i["text"]
        #         print(out)
        #         self._insert_message(out, "Doctor")
        #
        #         if out == "Can you send me a picture of your MRI?":
        #             self.entry.place(relwidth = 0.98, relheight = 0.06, rely = 0.008, relx = 0.011)
        #             self.add.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)
        #     except:
        #         None


    def _setup_main_window(self):
        self.window.title('Virtual Doctor')
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Doctor Message", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.0012)

        self.text = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                         font=FONT, padx=5, pady=5)
        self.text.place(relwidth=1, relheight=0.745, rely=0.08)
        self.text.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(self.text)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text.yview)
        scrollbar = Scrollbar(self.text, orient='horizontal')

        bottom_label = Label(self.window, bg=BG_GRAY, height=50)
        bottom_label.place(relwidth=1, rely=0.825)

        self.entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.entry.place(relwidth=0.98, relheight=0.06, rely=0.008, relx=0.011)
        self.entry.focus()
        self.entry.bind("<Return>", self._on_enter_pressed)






    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.cell = msg
        self.entry.delete(0,END)
        msg1 = f"{sender}: {msg}\n"
        self.text.configure(state=NORMAL)
        self.text.insert(END, msg1)
        self.text.configure(state=DISABLED)

    def add_original_image(self, filename):
        self.text.configure(state=NORMAL)
        global original_image
        self.img1 = Image.open(filename)

        original_image = ImageTk.PhotoImage(self.img1)
        self.text.image_create(END, image=original_image)
        self.text.insert(END, "\n")
        self.text.configure(state=DISABLED)

    def add_segmented_image(self):
        self.text.configure(state=NORMAL)
        global segmented_image
        img1 = Image.open("segmentedImage2.jpg")
        segmented_image = ImageTk.PhotoImage(img1)
        self.text.image_create(END, image=segmented_image)
        self.text.insert(END, "\n")
        self.text.configure(state=DISABLED)

if __name__ == '__main__':
    widget = Widget()
    widget.run()
