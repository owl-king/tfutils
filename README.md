# Terraform utils in NeoVim

tfutils is built for the enhance your workflow in neovim

![Create var quickly](https://media.giphy.com/media/l5zwatckCFFHYeHj3u/giphy.gif)

## Requirement
- python3.4 or newer

## Installation
With `packer` 
```lua
  use {
    'owl-king/tfutils',
    run = ':UpdateRemotePlugins'                                          
  }
```

## Usage
TBD

## Functions
Execute remote function with `:call`
- :call CreateTfVarFunction(variable, description)

## Roadmap
- [ ] Support more fields: `default`, `type`, `validation`, `sensitive` and `nullable`
- [ ] Autocreate tf var file base on file name or module
- [ ] Support visual mode
