using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RenderScreenToTexture : MonoBehaviour
{

    // Use this for initialization
    void Start()
    {
		
    }
	
    // Update is called once per frame
    void Update()
    {
    }

    public  Texture2D SnapScreenToTexture()
    {
        GameObject camObj = new GameObject();
        Camera cam = camObj.AddComponent<Camera>();
        cam.CopyFrom(Camera.main);
        camObj.transform.localPosition = Camera.main.transform.localPosition;
        camObj.transform.localRotation = Camera.main.transform.localRotation;
        camObj.transform.localScale = Camera.main.transform.localScale;

        int width = Screen.width;
        int height = Screen.height;
        RenderTexture renderTex = new RenderTexture(width, height, 24, RenderTextureFormat.ARGB32);
        renderTex.Create();


        cam.targetTexture = renderTex;



        cam.Render();

        //Camera.onPostRender -= PostRender;
        RenderTexture.active = renderTex;
        Texture2D newText = new Texture2D(width, height, TextureFormat.ARGB32, false);
        newText.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        newText.Apply();
        RenderTexture.active = null;
		Color32[] buf = newText.GetPixels32 ();

        GameObject.Destroy(camObj);
        return newText;

    }

}
