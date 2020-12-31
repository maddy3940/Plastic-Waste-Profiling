import platform # to print os version and name
import tkinter as tk
from tkinter.filedialog import askopenfilename
# from tkinter import simpledialog
import cv2 # imported to capture videos and images from user
from pil import Image,ImageTk
import os # for naming the files with indices
import shutil


"""
    add a feature of clicking live images and video,
    add hover effect for buttons                   
    check if webcam is open in each frame
"""

class PWP18():
    
    frame_top_bg = "#0A79DF"
    frame_nav = "#0A79DF"
    
    def __init__(self,root):
        self.root = root
        self.root.title("Deep Blue - PLASTIC WASTE PROFILING")
        # press escape to close the window
        self.root.bind('<Escape>',lambda e:self.root.destroy())
        self.cap = None
        # screen dimensions
        self.screen_height = 1000
        self.screen_width = 700
        
        # calculating x and y values
        x = (self.root.winfo_screenwidth() - self.screen_height)//2
#         y = (self.root.winfo_screenheight() - self.screen_width)//2
        
        self.root.geometry(f"{self.screen_height}x{self.screen_width}+{x}+{0}")
        self.root.resizable(False, False)
        # frame on top
        self.frame_top = tk.Frame(self.root,bg=self.frame_top_bg,height=(self.screen_height//4))
        self.frame_top.pack(side=tk.TOP,fill=tk.X)
        
        # create new frame for vertical navbar
        self.frame_nav = tk.Frame(self.root,
                                  bg=self.frame_nav,
                                  width = self.screen_width//4
                                  )
        self.frame_nav.pack(side = tk.LEFT,fill=tk.Y)
        self.frame_nav.propagate(0)
        
        # creating frame on right
        self.frame_right = tk.Frame(self.root,
                                    bg="blue",
                                    width = 100*(self.screen_width//4),
                                    relief = "ridge",
                                    bd="5"
                                    )
        self.frame_right.pack(side = tk.LEFT,fill=tk.BOTH)
        self.frame_right.propagate(0)

        
        # put pwp 18 on frame_top
        tk.Label(self.frame_top,
                text="Plastic Waste Profiling\n( Object Detection )",
                bg=self.frame_top_bg,
                padx = 20,
                pady = 20,
                font=('Monotype Corsiva',25,'bold'),
                ).pack(side = tk.LEFT)
        
        #put working os name and version
        tk.Label(self.frame_top,
                text=platform.system() + platform.release(),
                bg=self.frame_top_bg,
                padx = 50,
                pady = 20,
                font=('Helvetica',25)
                ).pack(side = tk.RIGHT)
        
        
        # add buttons to the navbar
        self.image_btn = tk.Button(self.frame_nav,text="Image",
                                   relief = 'ridge',
                                   pady = 50,
                                   bd=5,
                                   font = ('Cursive',20,'bold italic'),
                                   command = self.load_image
                                   )
        self.image_btn.pack(fill = tk.BOTH)
        
        
        self.video_btn = tk.Button(self.frame_nav,text="Video",
                                   relief = 'ridge',
                                   pady = 50,
                                   bd=5,
                                   font = ('Cursive',20,'bold italic'),
                                   command = self.load_video
                                   )
        self.video_btn.pack(fill = tk.BOTH)
        
        self.stats_btn = tk.Button(self.frame_nav,text="Stats",
                                   relief = 'ridge',
                                   pady = 50,
                                   bd=5,
                                   font = ('Cursive',20,'bold italic'),
                                   command = self.load_stats
                                   )
        self.stats_btn.pack(fill = tk.BOTH)
        
        self.admin_btn = tk.Button(self.frame_nav,text="Admin",
                                   relief = 'ridge',
                                   pady = 50,
                                   bd=5,
                                   font = ('Cursive',20,'bold italic'),
                                   
                                   )
        self.admin_btn.pack(fill = tk.BOTH)
        
        # add project description on initial screen
        tk.Label(self.frame_right,
                text=" Project Description ".center(100,'-'),
                bg="blue",
                font = ('Bookman Old style',20,'bold italic')).pack(pady = 10)
        
        self.definition = """ 
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
            
        """
        
        self.text = tk.Text(self.frame_right,bd=0,bg="blue",font=('Times New Roman',30))
        self.text.insert(tk.INSERT, self.definition)
        self.text.pack(padx = 10,fill=tk.BOTH)
        
        # disable editing in the text box
        self.text.bind('<Button-1>',lambda e:"break")
       
                           
        # giving notification after uploading an image
        
#         self.notify = tk.Label(self.frame_right,font = ('Normal',20,'bold'))
#         self.notify.pack()
        
    def clear_frame(self,frame):
        " clears all the widgets from the specified frame "
        for widget in frame.winfo_children():
            widget.destroy()
    
    def load_image(self):
        
        " loads all the widgets related to camera and images "
        
        self.clear_frame(self.frame_right)
        
        if(self.cap):
            self.cap.release()
        self.cap = cv2.VideoCapture(0)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,500)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,500)
        
        "Take path for dir"
        def capture():
            num = len(os.listdir())
            cv2.imwrite("image_"+str(num)+".jpg", self.frame)
            self.clear_frame(self.frame_right)
            tk.Label(self.frame_right,text="Thank you\nfor keeping your\n city clean !",
                     font=('Bookman Old Style',30,'bold italic'),
                     bg="blue"
                     ).pack(side = tk.TOP,pady=10)
            
        def store_into_file():
            "loading images from pc and copying them into given dir"
            im = askopenfilename()
            if(im == None):
                return
            
            newfilename = "image_"+str(len(os.listdir("C:\\Users\\Ashutosh\\My Documents\\LiClipse Workspace\\PWP18_ui\\images")))+".jpg"
            print(newfilename)
            shutil.copy(im,"C:\\Users\\Ashutosh\\My Documents\\LiClipse Workspace\\PWP18_ui\\images\\" + newfilename)
            self.clear_frame(self.frame_right)
            
            # creating a notification frame
            tk.Label(self.frame_right,text="Thank you\nfor keeping your\n city clean !",
                     font=('Bookman Old Style',30,'bold italic'),
                     bg="blue"
                     ).pack(side = tk.TOP,pady=10)
            
            self.cap.release()
            cv2.destroyAllWindows()
            
        
            
        self.lbl = tk.Label(self.frame_right,height = 500,width = self.screen_width,bg="blue",pady=5)
        self.lbl.pack(fill = tk.X,pady=2)
        
        self.capture = tk.Button(self.frame_right,text="Capture",bd=5,relief="ridge",
                                 font=('Monotype Corsiva',20,'bold'),
                                 command = capture)
        self.capture.pack(side = tk.LEFT,padx = (self.screen_width//5 + 30))
        
        self.load_from_gallery = tk.Button(self.frame_right,text="Load From Gallery",bd=5,
                                           relief="ridge",
                                           font=('Monotype Corsiva',20,'bold'),
                                           command = store_into_file
                                           )
        self.load_from_gallery.pack(side = tk.LEFT)
        
        def show_frame():
            _, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            self.cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
            self.img = Image.fromarray(self.cv2image)
            self.imgtk = ImageTk.PhotoImage(image=self.img)
            self.lbl.imgtk = self.imgtk
            self.lbl.configure(image = self.imgtk)
            self.lbl.after(10, show_frame)
            
        show_frame()

    
    def load_video(self):
        " every thing related to video capturing and storing "
        
        if(self.cap):
            self.cap.release()
        self.clear_frame(self.frame_right)
#         cv2.destroyAllWindows()
#         self.cap.release()
#         print(self.cap.isOpened()) # indicates that camera is closed
        self.cap = cv2.VideoCapture(0)
        
        self.flag = 0
        self.out = None
        def Start_Video():
            " set self.out "
            filename = "Video_"+str(len(os.listdir("C:\\Users\\Ashutosh\\My Documents\\LiClipse Workspace\\PWP18_ui\\videos")))
            self.out = "C:\\Users\\Ashutosh\\My Documents\\LiClipse Workspace\\PWP18_ui\\videos\\" + filename+".mp4"
            self.out = cv2.VideoWriter(self.out,
                                  -1,
                                  20.0,
                                  (640,480)
                                  )
        self.lbl = tk.Label(self.frame_right,height = 500,width = self.screen_width,bg="blue",pady=5)
        self.lbl.pack(fill = tk.X)
        
        
        def show_frame():
            _, self.frame = self.cap.read()
            if(self.out):
                self.out.write(self.frame)
            self.frame = cv2.flip(self.frame, 1)
            self.cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
            self.img = Image.fromarray(self.cv2image)
            self.imgtk = ImageTk.PhotoImage(image=self.img)
            self.lbl.imgtk = self.imgtk
            self.lbl.configure(image = self.imgtk)
            
            if(self.flag == 0):
                self.lbl.after(10, show_frame)
            elif(self.flag == 1):
                self.out.release()            
            
        show_frame()
        
        def Stop_Video():
            "stop the recording and release all the items "
            
            if(self.cap and self.out):
                self.flag = 1
            else:
                print("Camera not opened")
        
        self.video_start_btn = tk.Button(self.frame_right,
                                            text = "Start",
                                            
                                            padx=20,
                                            bd=5,
                                            font=('Monotype Corsiva',15,'bold'),
                                            command = Start_Video,
                                        )
        
        self.video_start_btn.pack(side=tk.LEFT,padx=100)
        
        self.video_stop_btn = tk.Button(self.frame_right,
                                        text = "upload",
                                        
                                        bd=5,
                                        padx=20,
                                        font=('Monotype Corsiva',15,'bold'),
                                        
                                        command = show_frame
                                        )
        
        self.video_stop_btn.pack(side=tk.LEFT,padx = 20)
        
        
        def load_from_gallery():
            "loading videos from pc and copying them into given dir"

            im = askopenfilename()
            newim = im
            extension = newim.split('.')[-1]
            
            if(im == None):
                return
            
            newfilename = "video_"+str(len(os.listdir("C:\\Users\\Ashutosh\\My Documents\\LiClipse Workspace\\PWP18_ui\\videos")))+"."+extension
            
            print(newfilename)
            shutil.copy(im,"C:\\Users\\Ashutosh\\My Documents\\LiClipse Workspace\\PWP18_ui\\videos\\" + newfilename)
            self.clear_frame(self.frame_right)
            
            # creating a notification frame
            tk.Label(self.frame_right,text="Thank you\nfor keeping your\n city clean !",
                     font=('Bookman Old Style',30,'bold italic'),
                     bg="blue"
                     ).pack(side = tk.TOP,pady=10)
            
            self.cap.release()
            cv2.destroyAllWindows()
        
        self.video_load_btn = tk.Button(self.frame_right,
                                        text = "load from gallery",
                                        padx=20,
                                        bd=5,
                                        font=('Monotype Corsiva',15,'bold'),
                                        command = load_from_gallery
                                        )
        
        self.video_load_btn.pack(side=tk.LEFT,padx=60)
        
        

    def load_stats(self):
        self.clear_frame(self.frame_right)
    
    
root = tk.Tk()

obj = PWP18(root)
root.mainloop()