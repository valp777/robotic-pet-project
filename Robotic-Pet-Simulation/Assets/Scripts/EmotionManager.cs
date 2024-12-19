using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class EmotionController : MonoBehaviour
{

    private string emotionUrl = "http://localhost:5000/detected_emotion";
    private string voiceUrl = "http://localhost:5000/talking_2_pet";
    private PetMovements petMovements;
 
    void Start()
    {
        petMovements = GetComponent<PetMovements>();
        StartCoroutine(GetEmotion());
        StartCoroutine(GetCommand());
    }

    IEnumerator GetEmotion()
    {
        while(true)
        {
            UnityWebRequest request = UnityWebRequest.Get(emotionUrl);
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

    IEnumerator GetCommand()
    {
        while(true)
        {
            // Create JSON data for the POST request to send voice command
            string jsonData = "{\"message\": \"Listen for command\"}";  // Example voice command
            UnityWebRequest request = new UnityWebRequest(voiceUrl, "POST");  // Send POST request to voice server
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonData);
            request.uploadHandler = new UploadHandlerRaw(jsonToSend);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                string response = request.downloadHandler.text;  // Get the response from the voice server
                Debug.Log("Command Response: " + response);

                // Parse the command (e.g., "sit", "sleep") from the response
                string command = ParseCommand(response);
                if (command != null)
                {
                    // display command detected
                    Debug.Log("Command detected: " + command);

                    // Trigger the appropriate movement based on the voice command
                    petMovements.TriggerMovement(command);  // Trigger movement or action based on the command
                }
            }
            else
            {
                Debug.LogError("Error: " + request.error);  // Log error if the request fails
            }

            yield return new WaitForSeconds(1);
        }

    }
    
    string ParseEmotion(string json)
    {
        return json.Contains("happy") ? "happy" : json.Contains("sad") ? "sad" : "neutral";
    }
    
    string ParseCommand(string json)
    {
        if (json.Contains("sit"))
            return "sit";
        else if (json.Contains("sleep"))
            return "sleep";
        else if (json.Contains("paw"))
            return "paw";
        else if (json.Contains("stand"))
            return "stand";
        else if (json.Contains("rollover"))
            return "rollover";
        return null;
    }

}
