#https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return bar

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    frame2 = frame
    width = 640
    height = 480
    cv2.rectangle(frame, (153, 115), (486, 364), (255,0,0),2)
    cv2.imshow('frame', frame)
    frame = frame2[120:360, 160:480]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.reshape((frame.shape[0] * frame.shape[1],3)) 

    cluster_num = KMeans(n_clusters=4) 
    cluster_num.fit(frame)

    hist = find_histogram(cluster_num)
    bar = plot_colors2(hist, cluster_num.cluster_centers_)
    plt.axis("off")
    plt.imshow(bar)

    fig.canvas.draw()
    fig.canvas.flush_events()
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()