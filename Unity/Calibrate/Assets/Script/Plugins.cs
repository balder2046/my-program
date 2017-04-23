using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using UnityEngine;

public class Plugins : MonoBehaviour
{

    // Use this for initialization
    void Start()
    {
		
    }
	
    // Update is called once per frame
    void Update()
    {
		
    }


    [DllImport("CalibratePlugin", EntryPoint = "GetOpenCVVersion" 
    )]
    static public extern int GetOpenCVVersion();
}
