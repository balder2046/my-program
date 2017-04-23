//
// Created by 赵磊 on 2017/4/21.
//
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "stdio.h"
using namespace cv;
typedef  unsigned char byte;
int main()
{
    int size = 18192;
    Mat matImage(size,size,CV_8UC1);
    // make zero
    for (int y = 0; y < size; ++y)
    {
        byte *rowbuf = matImage.ptr<byte>(y);
        for (int x = 0; x < size; ++x)
        {
            rowbuf[x] = 0;
        }
    }
    byte circle = 32;
    byte fan = 64;
    //circle
    int r = size / 2;
    int center = r;
    int circlecount = 0;
    for (int y = 0; y < size; ++y)
    {
        byte *rowbuf = matImage.ptr<byte>(y);
        for (int x = 0; x < size; ++x)
        {
            int dist = (x - center) * (x - center);
            dist += (y - center) * (y - center);
            if (dist < r * r)
            {
                rowbuf[x] += circle;
                circlecount++;
            }
        }
    }
    // fan
    r = size;

    for (int y = 0; y < size; ++y)
    {
        byte *rowbuf = matImage.ptr<byte>(y);
        for (int x = 0; x < size; ++x)
        {
            int dist = x * x;
            dist += y * y;
            if (dist < r * r)
            {
                rowbuf[x] += fan;
            }
        }
    }
    int count = 0;
    int totalcount = 0;
    for (int y = 0; y < size; ++y)
    {
        byte *rowbuf = matImage.ptr<byte>(y);
        for (int x = 0; x < size; ++x)
        {
            if (rowbuf[x] == circle)
                count++;
            totalcount++;
        }
    }
    printf("totalcount: %d count:%d ,scale %.20f",totalcount,count,(double)count / (double)totalcount);

    //namedWindow("question");
    //imshow("question",matImage);
  //  cvWaitKey(0);
    return 0;
}
