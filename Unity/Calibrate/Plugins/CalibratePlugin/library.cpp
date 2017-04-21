#include <iostream>
#include <vector>
#include "library.h"
/*
#include "opencv2/core/core.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "library.h"

#include <map>

using namespace cv;
typedef std::map<int,Mat> ImageMap;
ImageMap m_ImageMap;
static int Image_Count = 0;
int GenNewImageID()
{
    return ++Image_Count;
}
int  FindChessboardCorners(int imageid,int vertx,int verty,int flags,int corners[],int count[],int maxcount)
{
    *count= 0;
    auto iter_find = m_ImageMap.find(imageid);
    if (iter_find == m_ImageMap.end())
    {
        // 没有找到图像
        return 1;
    }
    Mat image = iter_find->second;
    std::vector<Point2f> _corners;
    bool found = findChessboardCorners(image,Size(vertx,verty),_corners);
    if (!found)
    {
        return -1;
    }

    for (int i = 0; i < _corners.size(); ++i)
    {
        corners[2 * i] = (int)_corners[i].x;
        corners[2 * i + 1] = (int)_corners[i].y;
    }
    *count = (int)_corners.size();

    return 0;
}
int PLUGIN_API CreateImage(int buf[],int width,int height)
{

    Mat mat = Mat(height,width,CV_8UC4);

    for (int row = 0; row < height; ++row)
    {
        Vec4b *rowbuf = mat.ptr<Vec4b>(row);
        int *srcbuf = buf + width * row;
        for (int col = 0; col <width; ++col)
        {
            unsigned char *pixel = (unsigned char *)(srcbuf + col);
            Vec4b temp = Vec4b(pixel[0],pixel[1],pixel[2],pixel[4]);
            rowbuf[col] = temp;
        }

    }
    int imageid = GenNewImageID();
    m_ImageMap[imageid] = mat;
    return imageid;
}
void hello() {
    std::cout << "Hello, World!" << std::endl;
}

void DeleteImage(int imageid) {
    ImageMap::iterator iter_find;
    iter_find = m_ImageMap.find(imageid);
    if (iter_find != m_ImageMap.end())
    {
        m_ImageMap.erase(iter_find);
    }
}
*/
int GetOpenCVVersion() {
    return 30;
}
