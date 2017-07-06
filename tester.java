import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import com.amazonaws.services.sqs.model.SendMessageRequest;

public class tester{
	public static void main(String[] args){
		// Send a message
		System.out.println("Sending a message to MyQueue.\n");
		sqs.sendMessage(new SendMessageRequest().withQueueUrl("https://sqs.us-east-1.amazonaws.com/258476513244/Temperature").withMessageBody("This is my message text."));
	}
}