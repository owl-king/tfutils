# A simple function for coding terrform in nvim

auto-tfvars is built for the painless of create terraform vars in `variables.tf` file. Multiple vars file are on the roadmap.

## Usage
Just `<leader>cv` to promt the function
- first arg is variable name
- second arg (optional) is description field

## Installation
With `packer` 
```lua
  use {                                                                       'owl-king/auto-tfvars',
    run = ':UpdateRemotePlugins'                                          
  }
```


## Roadmap
- [ ] Support more fields: `default`, `type`, `validation`, `sensitive` and `nullable`
- [ ] Autocreate tf var file base on file name or module
