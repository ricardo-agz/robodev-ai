## Tutorial Links:

Run a custom container is Azure:

https://learn.microsoft.com/en-us/azure/app-service/quickstart-custom-container?tabs=dotnet&pivots=container-linux-azure-portal


### Docker Build
`docker build -f ./Docker/Dockerfile -t neutrinogenerator.azurecr.io/generator-python-linux .`

### Deploy to Azure
`docker push neutrinogenerator.azurecr.io/generator-python-linux:latest`
