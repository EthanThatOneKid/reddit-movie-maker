void setup() {
  size(727, 409);
  String root = "C:\\Users\\acer\\Documents\\GitHub\\reddit-movie-maker\\db\\2019\\03\\26\\1553584300"; // args[0];
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

void renderPost(String title, String user, String body, String path) {
  
  background(26);
  int titleSize = 25;
  int userSize = 10;
  int bodySize = 20;
  int margin = 20;
  int padding = 10;
  int gimmeY = padding;
  float lineSpaceScalar = 1.2;
  
  // title
  fill(220);
  textSize(titleSize);
  text(title, margin, gimmeY, width - (2 * margin), height);
  gimmeY += ceil(textWidth(title) / (width - margin)) * lineSpaceScalar * (textDescent() + titleSize);
  gimmeY += padding;
  
  // user
  fill(70, 160, 210);
  textSize(userSize);
  text(user, margin, gimmeY);
  gimmeY += userSize + padding;
  
  // body
  fill(180);
  textSize(bodySize);
  text(body, margin, gimmeY, width - (2 * margin), 9999);
  
  gimmeY += (ceil(textWidth(body) / (width - margin)) + 3) * lineSpaceScalar * (textDescent() + bodySize);
  int offset = gimmeY - height;
  line(0, gimmeY, width, gimmeY);
  if (gimmeY > height) {
    translate(0, -offset);
  }
  save(path);
  
};
