import cv2 as cv
import mediapipe as mp


class HandDetector():

    def __init__(self, mode=False, Hands_num=2, Track_con=0.5, detection_con=0.5):
        self.Hands_num = Hands_num
        self.mode = mode
        self.Track_con = Track_con
        self.detection_con = detection_con
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def FindHands(self, frame):
        cvtrgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.handstracked = self.hands.process(cvtrgb)
        if self.handstracked.multi_hand_landmarks:
            for hand_marks in self.handstracked.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame, hand_marks, self.mpHands.HAND_CONNECTIONS)
        return frame

    def DisplayPoints(self, frame):
        lmst = []
        if self.handstracked.multi_hand_landmarks:
            hand = self.handstracked.multi_hand_landmarks
            for hand_marks in hand:
                for id, lm in enumerate(hand_marks.landmark):
                    h, w, c = frame.shape
                    cx1 = (int)(lm.x * w)
                    cy1 = (int)(lm.y * h)
                    lmst.append([id, cx1, cy1])
            return lmst


def main():
    cam = cv.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, frame = cam.read()
        frame = detector.FindHands(frame)
        cv.imshow("Video", frame)
        if cv.waitKey(20) & 0xFF == ord('d'):
            break


if __name__ == "__main__":
    main()