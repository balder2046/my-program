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
    // Use this for initialization
    void Start()
    {
		
    }
	
    // Update is called once per frame
    void Update()
    {
		
    }
}
