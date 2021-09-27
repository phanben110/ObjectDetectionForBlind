# this class to detect finger ussing handlamdmasks
import cv2
import mediapipe as mp
import time
import math

class handLandmarks:
    def __init__(self, mode=False , maxHands = 1 , detectionCon = 0.5 , trackCon=0.5) :
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode , self.maxHands, self.detectionCon, self.trackCon )
        self.mpDraw = mp.solutions.drawing_utils
        self.pointStore = []
        self.statusFinger = [None,None,None,None,None]
        self.results = None

    # function to store value point x,y each finger
    def storePoint( self, img  , handNo=0, draw=True) :
        xList = []
        yList = []
        box = []
        point8 = []

        self.pointStore = []
        if self.results :

            if self.results.multi_hand_landmarks:

                myHand =  self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate (myHand.landmark):
                    h,w,c = img.shape
                    cx,cy = int ( lm.x * w ) ,  int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)

                    self.pointStore.append([id,cx,cy])
                    #if draw and id==8:
                    #   cv2.circle( img , (cx,cy), 10 , (0,0,255), cv2.FILLED )
                    #    point8.append(cx)
                    #    point8.append(cy)


                xMin, xMax = min(xList)  , max (xList)
                yMin, yMax = min(yList)  , max (yList)
                box = xMin, yMin, xMax , yMax
        return self.pointStore  , box , point8

    # function to show finger in screen
    def showFinger( self, img , draw=True ) :
        imgRGB = cv2.cvtColor( img , cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print( results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks( img , handLms, self.mpHands.HAND_CONNECTIONS )
        return img
    def distance(self, pointA , pointB ) :
        x1 = pointA[1]
        y1 = pointA[2]
        x2 = pointB[1]
        y2 = pointB[2]
        return math.hypot(x2-x1,y2-y1)

    def findFingerUp(self, pointStore ) :
        # set example finger 1, index (8,7,6,5,0). put A = 0 , B = 5, C = 6, D = 7, E = 8
        listFinger = [[0,1,2,3,4],[0,5,6,7,8],[0,9,10,11,12],[0,13,14,15,16],[0,17,18,19,20]]
        if len(pointStore) != 0 :

            for i in range (5) :
                if i == 0 :
                    # call A is point 3, B is point 5, C is point 9 ,
                    F35 = self.distance( pointStore[3], pointStore[5] )
                    F59 = self.distance( pointStore[5], pointStore[9] )
                    F45 = self.distance( pointStore[4] , pointStore[5] )

                    if F35 > F59 and  F45 > F59*1.5  :
                        self.statusFinger[i] = 1
                    else:
                        self.statusFinger[i] = 0

                else :
                    AE = self.distance( pointStore[listFinger[i][0]], pointStore[listFinger[i][4]] )
                    AB = self.distance( pointStore[listFinger[i][0]], pointStore[listFinger[i][1]] )
                    AC = self.distance( pointStore[listFinger[i][0]], pointStore[listFinger[i][2]] )
                    AD = self.distance( pointStore[listFinger[i][0]], pointStore[listFinger[i][3]] )

                    if AE > AD and AD > AC and AC > AB :
                        self.statusFinger[i] = 1
                    elif AE < AD or AE < AC :
                        self.statusFinger[i] = 0
                    else :
                        self.statusFinger[i] = 2

            print ( f"status of finger  {self.statusFinger} " )
            total = sum(self.statusFinger)


            return self.statusFinger
        else :
            return 0
        #if ( len( pointStore ) != 0 ):
            #print ( pointStore )



if __name__ =="__main__" :
    ben = handLandmarks()
    pTime = 0
    cTime = 0
    video = 0 
    #video = 0
    cap = cv2.VideoCapture(video)
    while True :
        success, img = cap.read()
        ben.showFinger( img )
        pointList, box  = ben.storePoint ( img )
        ben.findFingerUp(pointList)
        #print ( box  )
        #print ( pointList[0] )
        print ( len ( box ) )
        if len ( box ) != 0 :

            cv2.rectangle( img , ( box[0] - 20 , box[1] - 20  ) , ( box[2] + 20 , box[3]+ 20  ) , (0,255,0),2 )
        cTime = time.time()
        fps = 1/( cTime - pTime )
        pTime = cTime
        cv2.putText( img , str( int ( fps ) ) , (10,70) , cv2.FONT_HERSHEY_PLAIN,3, (255, 0, 255 ) ,3 )
        cv2.imshow("image", img )
        cv2.waitKey(1)

