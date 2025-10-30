var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

 var database = new List<Dictionary<String, String>>();

app.MapGet("/", () => "Hello World!");

app.MapGet("/list", () => {
    return database;
});

app.MapPost("/create", async (HttpRequest request) => {
    var request_dict = await request.ReadFromJsonAsync<Dictionary<String, String>>();
    database.Add(request_dict);
});

app.Run();
