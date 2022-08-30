# A simple function for coding terrform in nvim

auto-tfvars is built for the painless of create terraform vars in `variables.tf` file. Multiple vars file are on the roadmap.

## Installation
With `packer` 
```lua
  use {
    'owl-king/auto-tfvars',
    run = ':UpdateRemotePlugins'                                          
  }
```

## Usage
Just `<leader>cv` to promt the function
- first arg is variable name
- second arg (optional) is description field

## Functions
Execute remote function with `:call`
- :call CreateTfVarFunction(variable, description)



## Roadmap
- [ ] Support more fields: `default`, `type`, `validation`, `sensitive` and `nullable`
- [ ] Autocreate tf var file base on file name or module
