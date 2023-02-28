# anchor-quick-launch
a pre-packaged software bundle that includes a stable and tested Solana binary and Anchor pre-installed

## Usage
Anchor-wrapper is a Python command line interface (CLI) to quickly create, manage and run a Solana-Anchor-ready environment.
You can use the anchor-wrapper init command to initialize a project:
```
anchor-wrapper init --type <program_type> <project_name> 
```

Or you can then use the anchor-wrapper start command to run a container which has the project folder mounted:
```
anchor-wrapper start <project_name> 
```

Where <program_type> is either program or client, and <project_name> is the name of your project.

Optional args:
- `--image`: Optionally, you can use the --image flag to set your preferred Docker image. The default is [ravthedoker/anchor-quick-launch](https://hub.docker.com/r/ravthedoker/anchor-quick-launch).
```
anchor-wrapper init --type <program_type> <project_name> --image <docker_image:tag> 
```
- `--port`: You can also choose to map a pair of host and container ports when running the Docker container.
```
anchor-wrapper init --type <program_type> <project_name> --port <host_port>:<container_port> 
```

- `--type`: 
  - To create a program in Python, run:
  ```
  anchor-wrapper init --type program <project_name>
  ```
  - To create a client using Next.js and Typescript, run:
  ```
  anchor-wrapper init --type client <project_name>
  ```

> Your project will be initialized in the current working directory and mapped to /app/<project_name> in the container.
## Technologies Used
- [Python](https://www.python.org/) 
- [PyInstaller](https://www.pyinstaller.org/) - Python lib to generate executables
- [pipenv](https://pipenv.pypa.io/en/latest/) - To mange packages
- [Docker](https://www.docker.com/) For creating base images which has stable Solana and Anchor pre-installed
