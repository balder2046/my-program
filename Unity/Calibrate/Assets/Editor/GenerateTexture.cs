using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System.IO;

public class GenerateTexture : MonoBehaviour
{

    [MenuItem("Texture/Chessboard")]
    static public void ChessBoardTextureGenerate()
    {
     
        // size: 128 * 128
        // block size: 8 * 8 , blocksize : 16 * 16
        int width = 512;
        int height = 512;
        // Create the 2d texture with mipmap
        Texture2D texture = new Texture2D(width, height, TextureFormat.ARGB32, true);
        // prepare the content buffer

        Color32[] buffer = new Color32[width * height ];
        Color32 black = new Color32(0, 0, 0, 255);
        Color32 white = new Color32(255, 255, 255, 255);
    
        int blocksize = width / 8;
        int index = 0;
        for (int y = 0; y < height; ++y)
        {
            for (int x = 0; x < width; ++x, ++index)
            {
                int blockx = x / blocksize;
                int blocky = y / blocksize;
                // blockx + blocky 是偶数的话, 那么就涂成黑色
                if ((blockx + blocky) % 2 == 0)
                {
                    buffer [index] = black;
                } else
                {
                    buffer [index] = white;
                }

            }
        }
        texture.SetPixels32(buffer);
        texture.Apply();
        string path = "Assets/Texture/autogen.png";
        string fullpath = Path.Combine(Directory.GetCurrentDirectory(), path);
        byte[] imgbuf = texture.EncodeToPNG();
        Debug.Log(fullpath);
        File.WriteAllBytes(fullpath, imgbuf);
        Debug.Log("Generate texture " + fullpath + " done!");

            

            
    }

    static Color32 Black = new Color32(0, 0, 0, 0);
    static Color32 Blue = new Color32(0, 0, 255, 255);
    static Color32 White = new Color32(255, 255, 255, 255);
    static Color32 Green = new Color32(0, 255, 0, 255);
    static Color32 Red = new Color32(255, 0, 0, 255);
    static Color32 Yellow = new Color32(255, 255, 0, 255);
    static Color32 Purple = new Color32(255, 0, 255, 255);


    [MenuItem("Texture/Disc-Red-Green")]
    static public void Disc_Red_Green()
    {
        
        GenerateCircusPattern(512, "disc-red-green.png", White, Red, Green, White);
    }

    [MenuItem("Texture/Disc-Red-Blue")]
    static public void Disc_Red_Blue()
    {

        GenerateCircusPattern(512, "disc-red-blue.png", White, Red, Blue, White);
    }

    [MenuItem("Texture/Disc-Red-Purple")]
    static public void Disc_Red_Purple()
    {

        GenerateCircusPattern(512, "disc-red-purple.png", White, Red, Purple, White);
    }

    [MenuItem("Texture/Disc-Green-Blue")]
    static public void Disc_Green_Blue()
    {

        GenerateCircusPattern(512, "disc-green-blue.png", White, Green, Blue, White);
    }

    [MenuItem("Texture/Disc-Green-Red")]
    static public void Disc_Green_red()
    {

		GenerateCircusPattern(512, "disc-green-red.png", White,  Green,Red, White);
    }

    [MenuItem("Texture/Disc-Green-Purple")]
    static public void Disc_Green_Purple()
    {

		GenerateCircusPattern(512, "disc-green-purple.png", White,  Green,Purple, White);
    }

    [MenuItem("Texture/Disc-Blue-Red")]
    static public void Disc_Blue_Red()
    {

        GenerateCircusPattern(512, "disc-blue-red.png", White, Blue,Red, White);
    }

    [MenuItem("Texture/Disc-Blue-Green")]
    static public void Disc_Blue_Green()
    {

        GenerateCircusPattern(512, "disc-blue-green.png", White, Blue, Green, White);
    }

    static int Sqr(int val)
    {
        return val * val;
    }

    static void GenerateCircusPattern(int size, string filename, Color32 colorTL, Color32 colorTR, Color32 colorBL, Color32 colorBR)
    {
        int width = size;
        int height = size;
        // Create the 2d texture with mipmap
        Texture2D texture = new Texture2D(width, height, TextureFormat.ARGB32, true);
        // prepare the content buffer

        Color32[] buffer = new Color32[width * height ];
        Color32 black = new Color32(0, 0, 0, 255);
        Color32 white = new Color32(255, 255, 255, 255);


        int index = 0;
        int radius = size / 2;
        int radiusq = radius * radius;
        int center = size / 2;
        for (int y = 0; y < height; ++y)
        {
            for (int x = 0; x < width; ++x, ++index)
            {
                // out the circle
                if (radiusq >= (Sqr(x - center) + Sqr(y - center)))
                {
                    if (y < center)
                    {
                        if (x < center)
                        {
                            buffer [index] = colorBL;
                        } else
                        {
                            buffer [index] = colorBR;
                        }
                    } else
                    {
                        if (x < center)
                        {
                            buffer [index] = colorTL;
                        } else
                        {
                            buffer [index] = colorTR;
                        }
                    }
                }

            }
        }
        texture.SetPixels32(buffer);
        texture.Apply();
        string path = "Assets/Texture/" + filename;
        string fullpath = Path.Combine(Directory.GetCurrentDirectory(), path);
        byte[] imgbuf = texture.EncodeToPNG();
        Debug.Log(fullpath);
        File.WriteAllBytes(fullpath, imgbuf);
        Debug.Log("Generate texture " + fullpath + " done!");
    }
    // Use this for initialization
    void Start()
    {
		
    }
	
    // Update is called once per frame
    void Update()
    {
		
    }
}
