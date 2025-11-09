using System.Text.Json;

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
    IResult result;
    try
    {
        var request_dict = await request.ReadFromJsonAsync<Dictionary<String, String>>();
        if (request_dict.Count == 0 || request_dict.Count > 2)
        {
            return Results.BadRequest("Empty JSON or extra input. Request key/value pair count: " + request_dict.Count);
        }
        if (!request_dict.ContainsKey("subject") || string.IsNullOrWhiteSpace(request_dict["subject"]))
        {
            result = Results.BadRequest("Missing/empty subject");
        }
        else if (!request_dict.ContainsKey("body") || string.IsNullOrWhiteSpace(request_dict["body"]))
        {
            result = Results.BadRequest("Missing/empty body");
        }
        else
        {
            database.Add(request_dict);
            var response_dict = new Dictionary<String, int>();
            // adjust later when there is data persistence to respond with actual id
            response_dict.Add("post_id", database.Count);
            result = Results.Ok(response_dict);
        }
    }
    catch (JsonException)
    {
        result = Results.BadRequest("Malformed JSON");
    }
    catch (Exception e)
    {
        Console.WriteLine(e);
        result = Results.StatusCode(500);
    }
    return result;
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
