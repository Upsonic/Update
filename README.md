# Upsonic Update

The cloud updating system for your python applications ! Control everything from one place and distribute all clients without effort

[Website](https://upsonic.co/upsonic-update) | [Discord](https://discord.gg/) | [Twitter](https://twitter.com/upsonicco)



## Installation
You can install Upsonic by pip3:

```console
pip3 install upsonic_update
```


# Implementing
In this point you can use any [Upsonic Cloud](https://docs.upsonic.co/upsonic_cloud.html).

```python
from upsonic_update import Upsonic_Update
from upsonic import Upsonic_Cloud
cloud = Upsonic_Cloud("YOUR_CLOUD_KEY")


updates = Upsonic_Update(cloud)

updates.pre_update("remove_lines") # Register your updates

# Define the updates
@cloud.active
def remove_lines(string):
    return string.replace("\n","")


updates.update() # Start to Update

```

And the console out is this:

```console
Updating: ['remove_lines']

remove_lines: OK

Updating Complated Without any Error
```




## Contributing
Contributions to Upsonic Update are welcome! If you have any suggestions or find a bug, please open an issue on the GitHub repository. If you want to contribute code, please fork the repository and create a pull request.

## License
Upsonic Update is released under the MIT License.

<h2 align="center">
    Contributors
</h2>
<p align="center">
    Thank you for your contribution!
</p>
<p align="center">
    <a href="https://github.com/Upsonic/Upsonic-Update/graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Upsonic/Upsonic-Update" />
    </a>
</p>
