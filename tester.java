// Send a message
System.out.println("Sending a message to MyQueue.\n");
sqs.sendMessage(new SendMessageRequest()
    .withQueueUrl("https://sqs.us-east-1.amazonaws.com/258476513244/Temperature")
    .withMessageBody("This is my message text."));