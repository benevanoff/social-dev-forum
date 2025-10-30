var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var database = new List<Dictionary<String, String>>();

app.MapGet("/", () => "Welcome to the developer's forum!");

app.MapGet("/list", () => {
    var response = new List<ListResponseItem>();
    for (int i = 0; i < database.Count; i++) {
        var item = new ListResponseItem();
        item.id = i+1;
        item.subject = database[i]["subject"];
        response.Add(item);
    }
    return response;
});

app.MapPost("/create", async (HttpRequest request) => {
    var request_dict = await request.ReadFromJsonAsync<Dictionary<String, String>>();
    database.Add(request_dict);

    var response_dict = new Dictionary<String, int>();
    response_dict.Add("post_id", database.Count);
    return response_dict;
});

app.MapGet("/post", (int id) => {
    return database[id-1];
});

app.Run();

public class ListResponseItem
{
    public int id { get; set; }
    public String subject { get; set; }
}
