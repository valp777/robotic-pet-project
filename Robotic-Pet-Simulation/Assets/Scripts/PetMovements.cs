using UnityEngine;

public class PetMovements : MonoBehaviour
{

    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }
    public void TriggerMovement(string emotion)
    {
        if (animator == null)
        {
            Debug.LogError("Animator component not found on the GameObject");
            return;
        }
        
        switch (emotion)
        {
            case "happy":
                TailWag();
                break;
            case "sad":
                MoveEars();
                break;
            case "fear":
                HeadTilt();
                break;
            default:
                NeutralPose();
                break;
        }
    }

    void TailWag()
    {
        animator.Play("TailWag");
        Debug.Log("Pet wags its tail!");
    }

    void MoveEars()
    {
        animator.Play("MoveEars");
        Debug.Log("Pet moves ears up and down to cheer up owner");
    }

    void HeadTilt()
    {
        animator.Play("HeadTilt");
        Debug.Log("Pet tilts head from curiosity to owner");
    }

    void NeutralPose()
    {
        animator.Play("NeutralPose");
        Debug.Log("Pet is sitting, tail still");
    }

}