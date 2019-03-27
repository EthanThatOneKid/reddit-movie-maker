String inputPath, savePath;
JSONObject inputData;

void setup() {
  inputPath = "C:/Users/acer/Documents/GitHub/reddit-movie-maker/db/2019/03/26/1553584300/data.json"; // args[0];
  savePath = args[1];
  inputData = loadJSONObject(inputPath);
  size(727, 409);
  // dim an array of strings
  for ([]String gimme : inputData) {
    println(gimme);
  }
  renderPost();
  //save(savePath);
  //exit();
};

void renderPost(String title, String user, String body) {
  
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
