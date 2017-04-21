#ifndef CALIBRATEPLUGIN_LIBRARY_H
#define CALIBRATEPLUGIN_LIBRARY_H

#ifdef _WIN32
#define PLUGIN_API __declspec(dllexport)
#else
#define PLUGIN_API
#endif

extern "C"
{
/*
    int PLUGIN_API FindChessboardCorners(int imageid,int vertx,int verty,int flags,int corners[],int count[],int maxcount);
    int PLUGIN_API CreateImage(int buf[],int width,int height);
    void PLUGIN_API DeleteImage(int imageid);
  */
    int PLUGIN_API GetOpenCVVersion();
}
void hello();

#endif