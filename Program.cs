var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

 var database = new List<int>();

app.MapGet("/", () => "Hello World!");

app.MapGet("/list", () => {
    return database;
});

app.MapPost("/create", () => {
    database.Add(database.Count + 1);
});

app.Run();
