using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using System.IO;
public class DemoController : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}
	public void WriteSceneMarkerfile(string filename)
	{
		StringBuilder builder = new StringBuilder();

	}
	public void OutputTransformToFile(string filename,Transform trans)
	{
		StringBuilder builder = new StringBuilder ();
		builder.AppendFormat ("Location,{0},{1},{2}\n", transform.position.x, transform.position.y, transform.position.z);
		builder.AppendFormat ("Rotation,{0},{1},{2}\n", transform.eulerAngles.x, transform.eulerAngles.y, transform.eulerAngles.z);
		File.WriteAllText (filename, builder.ToString ());
	}
	Transform[] FindAllMarkers()
	{
		GameObject markerNode = GameObject.Find ("Markers");
		if (markerNode != null) {
			int count = markerNode.transform.childCount;
			Transform [] childs = new Transform[count];
			for (int i = 0; i < count; ++i) {
				Transform marker = markerNode.transform.GetChild (i);
				childs [i] = marker;
			}
			return childs;
		}
		return null;
	}
}
