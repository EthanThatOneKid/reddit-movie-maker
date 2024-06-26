int titleSize;
int userSize;
int bodySize;
int margin;
int maxWidth;
int padding;
float lineSpaceScalar;
float fontSizeScalar;
PImage bgImg;

void setup() {
  
  fontSizeScalar = 1.8;
  lineSpaceScalar = 1.15;

  titleSize = int(25 * fontSizeScalar);
  userSize = int(10 * fontSizeScalar);
  bodySize = int(20 * fontSizeScalar);
  margin = 20;
  maxWidth = width - (2 * margin);
  padding = int(10 * fontSizeScalar);
  
  String bgImgDir = String.format("%s/static/backgrounds/", sketchPath());
  int bgImgIndex = floor(random(0, listFiles(bgImgDir).length));
  String bgImgPath = String.format("%s/%d.jpg", bgImgDir, bgImgIndex);
  println(String.format("Using background image #%d", bgImgIndex));
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
      
      String savePath = String.format("%s/photos/%s/%s.png", root, i, j);
      accumulator += sentences.getString(j) + " ";
      renderPost(title, user, accumulator, savePath);
      
      // saving the thumbnail
      if (i == 0 && j == 0) {
        savePath = String.format("%s/thumb.png", root);
        renderPost(title, user, accumulator, savePath);
      }
      
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

void renderPost(String title, String user, String body, String path) {
  
  tint(16, 39, 66);
  image(bgImg, 0, 0);

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
