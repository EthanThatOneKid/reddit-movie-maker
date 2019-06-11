int titleSize;
int userSize;
int bodySize;
int margin;
int maxWidth;
int padding;
float lineSpaceScalar;
PImage bgImg;

void setup() {

  titleSize = 25;
  userSize = 10;
  bodySize = 20;
  margin = 20;
  maxWidth = width - (2 * margin);
  padding = 10;
  lineSpaceScalar = 1.15;
  
  int bgImgIndex = floor(random(listFiles(sketchPath()).length));
  String bgImgPath = String.format("%s/static/backgrounds/%n.jpg", sketchPath(), bgImgIndex);
  bgImg = loadImage(bgImgPath);

  size(1280, 720);
  String root = args[0];
  String inputPath = String.format("%s\\data.json", root);
  JSONObject rawInputData = loadJSONObject(inputPath);
  JSONArray posts = rawInputData.getJSONArray("data");
  
  for (int i = 0; i < posts.size(); i++) {
    
    JSONArray post = posts.getJSONArray(i);
    String title = post.getString(0);
    String user = String.format("u/%s", post.getString(1));
    JSONArray sentences = post.getJSONArray(2);
    String accumulator = "";
    
    for (int j = 0; j < sentences.size(); j++) {
      
      String savePath = String.format("%s\\photos\\%s\\%s.png", root, i, j);
      accumulator += sentences.getString(j) + " ";
      renderPost(title, user, accumulator, savePath);
      
    }
    
  }
  
  exit();
  
};

int[] getRenderSummary(String title, String user, String body) {

  int[] result = new int[4];
  int gimmeY = margin;

  // title
  result[1] = gimmeY;

  // user
  textSize(titleSize);
  gimmeY += ceil(textWidth(title) / maxWidth) * lineSpaceScalar * (textDescent() + titleSize);
  gimmeY += padding;
  result[2] = gimmeY;

  // body
  textSize(userSize);
  gimmeY += userSize + padding;
  result[3] = gimmeY;

  // offset
  textSize(bodySize);
  gimmeY += (ceil(textWidth(body) / maxWidth) + 3) * lineSpaceScalar * (textDescent() + bodySize);
  int offset = gimmeY - height;
  if (offset < 0) offset = 0;
  result[0] = offset;
  return result;

};

void renderThumbnail(String title, String subreddit, String path) {
  // TODO: some shit
};

void renderPost(String title, String user, String body, String path) {
  
  image(bgImg, 0, 0);
  background(51, 51, 51, 51);

  int[] renderPositions = getRenderSummary(title, user, body);
  int offset = renderPositions[0];
  int titleY = renderPositions[1] - offset;
  int userY = renderPositions[2] - offset;
  int bodyY = renderPositions[3] - offset;

  // title
  fill(220);
  textSize(titleSize);
  text(title, margin, titleY, maxWidth, height);

  // user
  fill(70, 160, 210);
  textSize(userSize);
  text(user, margin, userY);

  // body
  fill(180);
  textSize(bodySize);
  text(body, margin, bodyY, maxWidth, 9999);
  
  // save
  save(path);

};
