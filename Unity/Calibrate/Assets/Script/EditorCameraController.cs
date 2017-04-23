using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class EditorCameraController : MonoBehaviour
{

    // Use this for initialization
    Camera camera;
    public float speedMove = 2.0f;
    public float rotateSpeed = 8.0f;

    void Start()
    {
        camera = GetComponent<Camera>();
        int version = Plugins.GetOpenCVVersion();
        Debug.Log("the version is " + version);
    }
	
    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButton(1))
        {
            Vector3 offset = Vector3.zero;
            if (Input.GetKey(KeyCode.W))
            {
                offset.z = 1.0f;
            } else if (Input.GetKey(KeyCode.S))
            {
                offset.z = -1.0f;
            } else if (Input.GetKey(KeyCode.A))
            {
                offset.x = -1.0f;
            } else if (Input.GetKey(KeyCode.D))
            {
                offset.x = 1.0f;
            } else if (Input.GetKey(KeyCode.Q))
            {
                offset.y = -1.0f;
            } else if (Input.GetKey(KeyCode.E))
            {
                offset.y = 1.0f;
            }
            transform.Translate(offset * speedMove * Time.deltaTime, Space.Self);
            Vector3 rotateAngles = Vector3.zero;
            rotateAngles.x = -Input.GetAxis("Mouse Y") * rotateSpeed;
            rotateAngles.y = Input.GetAxis("Mouse X") * rotateSpeed;
            //transform.Rotate(rotateAngles, Space.Self);
            Vector3 oldRotate = transform.localEulerAngles;
            oldRotate += rotateAngles;
            transform.localEulerAngles = oldRotate;

        }
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Texture2D tex = SnapScreenToTexture();
            byte[] buffer = tex.EncodeToJPG();
            System.IO.File.WriteAllBytes("test.jpg", buffer);
        }
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

        GameObject.Destroy(camObj);
        return newText;

    }
}