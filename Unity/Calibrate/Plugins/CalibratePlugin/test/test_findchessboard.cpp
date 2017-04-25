//
// Created by 赵磊 on 2017/4/25.
//
#include "opencv2/opencv.hpp"
#include <vector>
#include "stdio.h"
using namespace cv;

int main()
{
    Mat inImage;
    inImage = imread("test.jpg",IMREAD_COLOR);

    bool findboard = false;
    std::vector<Point2f> cornors;
    findboard = findChessboardCorners(inImage,Size(7,7),cornors,CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE
                                                                + CALIB_CB_FAST_CHECK);
    if (!findboard)
    {
        printf("There is no chessboard!!!!");
        return 1;
    }
    int index = 0;
    for (auto iter = cornors.begin(); iter != cornors.end(); ++iter)
    {
        printf("the point %d is (%.2f,%.2f)\n",index,iter->x,iter->y);
                index++;
    }
    namedWindow("Image");
    drawChessboardCorners(inImage,Size(7,7),cornors,findboard);
    circle(inImage,Point(500,500),5,Scalar(255.0,0,0));

    imshow("Image",inImage);
    bool bNext =false;
    auto iter = cornors.begin();

    while(true)
    {
        if (bNext)
        {
            if (iter == cornors.end()) return 0;
            Point pos((int)iter->x, (int)iter->y);
            Mat frame;
            inImage.copyTo(frame);
            circle(frame,pos,5,Scalar(0,255,0));
            imshow("Image",frame);
            bNext = false;
            iter++;

        }


        int code = waitKey(200);
        if (code == 27)
            return 1;
        if (code > 0)
        {
            bNext = true;
        }
    }

    return 0;
}
