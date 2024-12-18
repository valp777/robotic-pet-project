using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class EmotionController : MonoBehaviour
{

    private string apiUrl = "http://localhost:5000/detected_emotion";
    private PetMovements petMovements;
 
    void Start()
    {
        petMovements = GetComponent<PetMovements>();
        StartCoroutine(GetEmotion());
    }

    IEnumerator GetEmotion()
    {
        while(true)
        {
            UnityWebRequest request = UnityWebRequest.Get(apiUrl);
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                string response = request.downloadHandler.text;
                string emotion = ParseEmotion(response);
                petMovements.TriggerMovement(emotion);
            }
            else 
            {
                Debug.LogError("Error: " + request.error);
            }
            yield return new WaitForSeconds(7); // check emotion every 7 seconds
        }
    }
    
    string ParseEmotion(string json)
    {
        return json.Contains("happy") ? "happy" : json.Contains("sad") ? "sad" : "neutral";
    }

}


