//String title = "A VERY VERY LONG TITLE"; // args[1]
//String user = "u/EthanThatOneKid"; // args[2]
//String body = "Hello World"; // args[3]
//String savePath = "./recent/1.png"; // args[4]

String title = args[0];
String user = args[1];
String body = args[2];
String savePath = args[3];

void setup() {
  println(title);
  println(user);
  println(body);
  println(title);
  size(727, 409);
  //renderPost();
  //save(savePath);
  //println("saved under " + savePath);
  exit();
};

void renderPost() {
  
  background(0);
  int titleSize = 25;
  int userSize = 10;
  int bodySize = 20;
  int margin = 10;
  int padding = 10;
  int gimmeY = padding;
  float lineSpaceScalar = 1.2;
  
  // title
  fill(240, 253, 253);
  textSize(titleSize);
  text(title, margin, gimmeY, width - margin, height);
  gimmeY += ceil(textWidth(title) / (width - margin)) * lineSpaceScalar * (textDescent() + titleSize);
  gimmeY += padding;
  
  // user
  fill(70, 160, 210);
  textSize(userSize);
  text(user, margin, gimmeY);
  gimmeY += userSize + padding;
  
  // body
  fill(240, 253, 253);
  textSize(bodySize);
  text(body, margin, gimmeY, width - margin, height - gimmeY);
  
};
