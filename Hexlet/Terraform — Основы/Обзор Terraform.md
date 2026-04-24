---
tags: [terraform, infrastructure, hexlet]
source: "Terraform — Основы"
---

# Обзор Terraform

  * Подготовка
  * Инициализация
  * Описание инфраструктуры
  * Создание
  * Собирая все вместе



В этом уроке мы рассмотрим типовой рабочий процесс с использованием Terraform без погружения в детали. Опишем небольшую инфраструктуру и поработаем с ней, развернем, обновим и удалим. А в следующих уроках, рассмотрим все это подробно.

## Подготовка

На протяжении всего курса, мы будем описывать нашу инфраструктуру в репозитории, который станет частью вашего портфолио. Для этого создайте на Github репозиторий _hexlet-terraform_ и клонируйте его себе на компьютер. Все дальнейшие команды будут выполняться внутри этого репозитория.

Теперь установите Terraform по этой ссылке. Проверьте что он работает: 
    
    
    terraform -v
    Terraform v1.7.1
    

Зарегистрируйтесь в Yandex Cloud. На этой странице описано как получить OAuth-токен. Сделайте запрос и получите ключ, который понадобится Terraform для выполнения удаленных команд.

## Инициализация

Перед началом работы с Terraform, нужно определиться с облаком, которое будет использоваться. Все примеры курса даются в Yandex Cloud, но вы можете выбрать любое другое облако, которое вам по душе. Правда для этого придется самостоятельно копаться в документации, чтобы повторять за тем, что дается в уроке.

Когда облако выбрано, нужно найти его в списке провайдеров и перейти в документацию. Либо можно посмотреть документацию в самом облачном провайдере. Здесь описано, как инициализировать работу с ним.

Зачем нужен провайдер? Провайдер это модуль Terraform, который умеет работать с конкретным облаком. Как только он подключается к проекту, внутри появляются команды для взаимодействия с его сервисами.

Для подключения провайдера Yandex Cloud, создайте файл _.terraformrc_ и добавьте в него содержимое: 
    
    
    provider_installation {
      network_mirror {
        url = "https://terraform-mirror.yandexcloud.net/"
        include = ["registry.terraform.io/*/*"]
      }
      direct {
        exclude = ["registry.terraform.io/*/*"]
      }
    }
    

Эти данные содержат информацию об источнике, и которого будет устанавливаться провайдер.

Затем создайте файл _main.tf_ и добавьте в него такое содержимое: 
    
    
    // main.tf - имя файла выбрано произвольно, важно только расширение
    terraform {
      required_providers {
        yandex = {
          source = "yandex-cloud/yandex"
        }
      }
      required_version = ">= 0.13"
    }
    
    // Terraform должен знать ключ, для выполнения команд по API
    
    // Определение переменной, которую нужно будет задать
    variable "yc_token" {}
    
    provider "yandex" {
      zone = "ru-central1-a"
      token = var.yc_token
    }
    

Помимо указания списка провайдеров, мы описываем переменную `yc_token`, которая записывается в аттрибут `token` провайдера _yandex_. Это ключ необходим Terraform для выполнения команд по API. Значение ключа указывать в конфигурации нельзя, иначе, кто-нибудь сможет с его помощью выполнить любой код на YandexCloud, включая полное уничтожение всей инфраструктуры.

Для работы с секретами, Terraform предлагает создавать файлы с расширением _*.auto.tfvars_ , которые добавляются в _.gitignore_. Сам ключ, при этом, можно хранить в зашифрованном виде в Ansible Vault.

Создадим файл _secrets.auto.tfvars_ , в котором описываются переменные, содержащие секретные данные. Добавим туда наш ключ как значение переменной `yc_token`: 
    
    
    // Terraform автоматически подгрузит этот файл
    yc_token = "<тут секретный ключ>"
    

После того как провайдер добавлен, нужно выполнить инициализацию: 
    
    
    terraform init
    
    Initializing the backend...
    
    Initializing provider plugins...
    - Finding latest version of yandex-cloud/yandex...
    - Installing yandex-cloud/yandex v0.106.0...
    - Installed yandex-cloud/yandex v0.106.0 (self-signed, key ID E40F590B50BB8E40)
    
    Partner and community providers are signed by their developers.
    If you'd like to know more about provider signing, you can read about it here:
    https://www.terraform.io/docs/cli/plugins/signing.html
    
    Terraform has created a lock file .terraform.lock.hcl to record the provider
    selections it made above. Include this file in your version control repository
    so that Terraform can guarantee to make the same selections by default when
    you run "terraform init" in the future.
    
    Terraform has been successfully initialized!
    

Во время инициализации скачивается код провайдера в директорию _.terraform_. Эта служебная директория, содержимое которой нам не важно, поэтому ее добавляют в _.gitignore_.

Инициализация выполняется каждый раз, когда репозиторий клонируется заново или обновляются версии зависимостей. Несмотря на название, команда `terraform init` больше похожа на установку зависимостей в JavaScript с помощью `npm install`.

Кроме _.terraform_ , в директории с проектом оказывается файл _.terraform.lock.hcl_.

## Описание инфраструктуры

На странице документации провайдера, слева меню, в котором есть список возможностей провайдера. Мы начнем с самой базовой - создании сервера.

В терминах Terraform _yandex_compute_instance_ называется ресурсом. Это то, чем мы управляем в нашем облаке. Создадим сервер: 
    
    
    terraform {
      required_providers {
        yandex = {
          source = "yandex-cloud/yandex"
        }
      }
      required_version = ">= 0.13"
    }
    
    variable "yc_token" {}
    
    provider "yandex" {
      zone = "ru-central1-a"
      token = var.yc_token
    }
    
    resource "yandex_compute_instance" "default" {
      name        = "test"
      platform_id = "standard-v1"
      zone        = "ru-central1-a"
      folder_id   = "<идентификатор каталога>"
    
      resources {
        cores  = 2
        memory = 4
      }
    
      boot_disk {
        disk_id = yandex_compute_disk.default.id
      }
    
      network_interface {
        subnet_id = "${yandex_vpc_subnet.default.id}"
      }
    
      metadata = {
        ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
      }
    }
    
    resource "yandex_vpc_network" "default" {
      folder_id = "<идентификатор каталога>"
    }
    
    resource "yandex_vpc_subnet" "default" {
      zone           = "ru-central1-a"
      network_id     = "${yandex_vpc_network.default.id}"
      v4_cidr_blocks = ["10.5.0.0/24"]
      folder_id      = "<идентификатор каталога>"
    }
    
    resource "yandex_compute_disk" "default" {
      name     = "disk-name"
      type     = "network-ssd"
      zone     = "ru-central1-a"
      image_id = "fd83s8u085j3mq231ago" // идентификатор образа Ubuntu
      folder_id = "<идентификатор каталога>"
    
      labels = {
        environment = "test"
      }
    }
    

Для создания сервера, нам пришлось создать дополнительные ресурсы _yandex_vpc_network_ , _yandex_vpc_subnet_ , _yandex_compute_disk_.

Описание аргументов _resources_ , _boot_disk_ и других идет в документации сразу после примера в секции _Argument Reference_. Там же указано какие из них обязательные, а какие нет. С другой стороны, в этом разделе не хватает информации о возможных значениях. Откуда брать значения для _platform_id_ или _cores_? Иногда в документации есть ссылка на страницу с возможными значениями, но это бывает не всегда. К сожалению здесь не остается ничего другого, как пытаться найти эту информацию в документации облачного провайдера. Здесь обычно помогает Google.

Ресурсы требуют указания _folder_id_ — это ваш каталог внутри которого будет создан ресурс. Его идентификатор можно найти в консоли Yandex Cloud. Если каталог не создан, создайте его.

Язык описания инфраструктуры отдаленно напоминает JSON и интуитивно понятен в большинстве ситуаций. Главное что нужно понимать, он описывает не команды, а состояние того, что мы хотим получить в конце. Это значит что порядок описания инфраструктуры не имеет значения, Terraform все равно сделает изменения в том порядке, в котором нужно.

Инфраструктуру можно описывать в любых файлах с расширением _*.tf_. Terraform самостоятельно их загружает и вычисляет порядок, в котором надо выполнять изменения. Для простоты мы все делаем в файле _main.tf_. Когда кода много, его удобно раскладывать по разным файлам.

## Создание

Теперь, когда ресурсы описаны, можно их создать. Делается это в два шага. Сначала нам показывают план изменений и если он соответствует нашим ожиданиям, то мы подтверждаем его выполнение и Terraform делает это 
    
    
    terraform apply
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
    Terraform will perform the following actions:
    
      # yandex_compute_disk.default will be created
      + resource "yandex_compute_disk" "default" {
          + block_size  = 4096
          + created_at  = (known after apply)
          + folder_id   = "<идентификатор каталога>"
          + id          = (known after apply)
          + image_id    = "fd83s8u085j3mq231ago"
          + labels      = {
              + "environment" = "test"
            }
          + name        = "disk-name"
          + product_ids = (known after apply)
          + size        = 150
          + status      = (known after apply)
          + type        = "network-ssd"
          + zone        = "ru-central1-a"
        }
    
      # yandex_compute_instance.default will be created
      + resource "yandex_compute_instance" "default" {
          + created_at                = (known after apply)
          + folder_id                 = "<идентификатор каталога>"
          + fqdn                      = (known after apply)
          + gpu_cluster_id            = (known after apply)
          + hostname                  = (known after apply)
          + id                        = (known after apply)
          + maintenance_grace_period  = (known after apply)
          + maintenance_policy        = (known after apply)
          + metadata                  = {
              + "ssh-keys" = "<тут публичный ssh-ключ>"
            }
          + name                      = "test"
          + network_acceleration_type = "standard"
          + platform_id               = "standard-v1"
          + service_account_id        = (known after apply)
          + status                    = (known after apply)
          + zone                      = "ru-central1-a"
    
          + boot_disk {
              + auto_delete = true
              + device_name = (known after apply)
              + disk_id     = (known after apply)
              + mode        = (known after apply)
            }
    
          + network_interface {
              + index              = (known after apply)
              + ip_address         = (known after apply)
              + ipv4               = true
              + ipv6               = (known after apply)
              + ipv6_address       = (known after apply)
              + mac_address        = (known after apply)
              + nat                = false
              + nat_ip_address     = (known after apply)
              + nat_ip_version     = (known after apply)
              + security_group_ids = (known after apply)
              + subnet_id          = (known after apply)
            }
    
          + resources {
              + core_fraction = 100
              + cores         = 2
              + memory        = 4
            }
        }
    
      # yandex_vpc_network.default will be created
      + resource "yandex_vpc_network" "default" {
          + created_at                = (known after apply)
          + default_security_group_id = (known after apply)
          + folder_id                 = "<идентификатор каталога>"
          + id                        = (known after apply)
          + labels                    = (known after apply)
          + name                      = (known after apply)
          + subnet_ids                = (known after apply)
        }
    
      # yandex_vpc_subnet.default will be created
      + resource "yandex_vpc_subnet" "default" {
          + created_at     = (known after apply)
          + folder_id      = "<идентификатор каталога>"
          + id             = (known after apply)
          + labels         = (known after apply)
          + name           = (known after apply)
          + network_id     = (known after apply)
          + v4_cidr_blocks = [
              + "10.5.0.0/24",
            ]
          + v6_cidr_blocks = (known after apply)
          + zone           = "ru-central1-a"
        }
    
    Plan: 4 to add, 0 to change, 0 to destroy.
    
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.
    
      Enter a value: 
    
    

Очень важно убедиться, что здесь нет ничего опасного, например удаление или пересоздание каких-то ресурсов, которые нельзя трогать. В этом смысле, Terraform максимально опасный инструмент. Неверно примененный план может привести к полной потере всего проекта включая бекапы.

Если нас все устраивает, то нужно набрать _yes_. Создание серверов займет какое-то время. Terraform выполняет все операции синхронно, поэтому он закончит работу только после внесения всех изменений. 
    
    
      Enter a value: yes
    
    # Для удобства здесь видны имена, которые задаются в конфигурации
    yandex_vpc_network.default: Creating...
    yandex_compute_disk.default: Creating...
    yandex_vpc_network.default: Creation complete after 3s [id=enp3kbem2tc27rl1p3cr]
    yandex_vpc_subnet.default: Creating...
    yandex_vpc_subnet.default: Creation complete after 1s [id=e9b313hmo8022as59e1n]
    yandex_compute_disk.default: Still creating... [10s elapsed]
    yandex_compute_disk.default: Creation complete after 12s [id=fhmu797gh7d23f2ekna2]
    yandex_compute_instance.default: Creating...
    yandex_compute_instance.default: Still creating... [10s elapsed]
    yandex_compute_instance.default: Still creating... [20s elapsed]
    yandex_compute_instance.default: Creation complete after 26s [id=fhmdbscqlcgdgn0p8id6]
    
    Apply complete! Resources: 4 added, 0 changed, 0 destroyed.
    

Если все прошло успешно, то зайдите в личный кабинет Yandex Cloud и убедитесь, что сервер создан. Правда магия?

После того как Terraform выполнит изменения, он создает и затем обновляет файл _terraform.tfstate_. Этот файл хранит состояние инфраструктуры на текущий момент. Зачем это нужно? С его помощью Terraform вычисляет разницу между тем, что мы хотим получить в итоге и тем что есть сейчас. Без него Terraform будет считать, что инфраструктура каждый раз создается заново. Этот файл обычно не хранят в репозитории, так как вместе с состоянием в нем могут быть чувствительные данные вроде паролей и токенов. Более того, с этим файлом в один момент времени может работать только один человек, иначе Terraform не сможет правильно оценить текущую инфраструктуру. Для этого используют специальные сервисы, которые хранят файл состояния на удаленном сервере

Кроме _terraform.tfstate_ Terraform создает файлы бекапы с расширением _*.backup_. Их нужно добавить в _.gitignore_.

Ну и наконец, давайте попробуем все удалить: 
    
    
    terraform destroy
    
    terraform destroy
    digitalocean_droplet.web1: Refreshing state... [id=292822008]
    digitalocean_droplet.web2: Refreshing state... [id=292822010]
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
    following symbols:
      - destroy
    
    Terraform will perform the following actions:
    
      # yandex_compute_disk.default will be destroyed
      - resource "yandex_compute_disk" "default" {
          - block_size  = 4096 -> null
          - created_at  = "2024-01-31T12:34:31Z" -> null
          - folder_id   = "<идентификатор каталога>" -> null
          - id          = "fhm3acu0uitbelemhm0k" -> null
          - image_id    = "fd83s8u085j3mq231ago" -> null
          - labels      = {
              - "environment" = "test"
            } -> null
          - name        = "disk-name" -> null
          - product_ids = [
              - "f2eth1eavhqoh47mqj08",
            ] -> null
          - size        = 150 -> null
          - status      = "ready" -> null
          - type        = "network-ssd" -> null
          - zone        = "ru-central1-a" -> null
    
          - disk_placement_policy {}
        }
    
      # yandex_compute_instance.default will be destroyed
      - resource "yandex_compute_instance" "default" {
          - created_at                = "2024-01-31T12:34:47Z" -> null
          - folder_id                 = "<идентификатор каталога>" -> null
          - fqdn                      = "fhmpldmndpo4ufoji6gf.auto.internal" -> null
          - id                        = "fhmpldmndpo4ufoji6gf" -> null
          - labels                    = {} -> null
          - metadata                  = {
              - "ssh-keys" = "<тут публичный ssh-ключ>"
            } -> null
          - name                      = "test" -> null
          - network_acceleration_type = "standard" -> null
          - platform_id               = "standard-v1" -> null
          - status                    = "running" -> null
          - zone                      = "ru-central1-a" -> null
    
          - boot_disk {
              - auto_delete = true -> null
              - device_name = "fhm3acu0uitbelemhm0k" -> null
              - disk_id     = "fhm3acu0uitbelemhm0k" -> null
              - mode        = "READ_WRITE" -> null
    
              - initialize_params {
                  - block_size = 4096 -> null
                  - image_id   = "fd83s8u085j3mq231ago" -> null
                  - name       = "disk-name" -> null
                  - size       = 150 -> null
                  - type       = "network-ssd" -> null
                }
            }
    
          - metadata_options {
              - aws_v1_http_endpoint = 1 -> null
              - aws_v1_http_token    = 2 -> null
              - gce_http_endpoint    = 1 -> null
              - gce_http_token       = 1 -> null
            }
    
          - network_interface {
              - index              = 0 -> null
              - ip_address         = "10.5.0.8" -> null
              - ipv4               = true -> null
              - ipv6               = false -> null
              - mac_address        = "d0:0d:19:ab:6d:76" -> null
              - nat                = false -> null
              - security_group_ids = [] -> null
              - subnet_id          = "e9bc80kd45lfmfq2fq0d" -> null
            }
    
          - placement_policy {
              - host_affinity_rules       = [] -> null
              - placement_group_partition = 0 -> null
            }
    
          - resources {
              - core_fraction = 100 -> null
              - cores         = 2 -> null
              - gpus          = 0 -> null
              - memory        = 4 -> null
            }
    
          - scheduling_policy {
              - preemptible = false -> null
            }
        }
    
      # yandex_vpc_network.default will be destroyed
      - resource "yandex_vpc_network" "default" {
          - created_at                = "2024-01-31T12:34:31Z" -> null
          - default_security_group_id = "enp2dag2iedkjuak3pkn" -> null
          - folder_id                 = "<идентификатор каталога>" -> null
          - id                        = "enpvpoj117va949tjmae" -> null
          - labels                    = {} -> null
          - subnet_ids                = [
              - "e9bc80kd45lfmfq2fq0d",
            ] -> null
        }
    
      # yandex_vpc_subnet.default will be destroyed
      - resource "yandex_vpc_subnet" "default" {
          - created_at     = "2024-01-31T12:34:33Z" -> null
          - folder_id      = "<идентификатор каталога>" -> null
          - id             = "e9bc80kd45lfmfq2fq0d" -> null
          - labels         = {} -> null
          - network_id     = "enpvpoj117va949tjmae" -> null
          - v4_cidr_blocks = [
              - "10.5.0.0/24",
            ] -> null
          - v6_cidr_blocks = [] -> null
          - zone           = "ru-central1-a" -> null
        }
    
    Plan: 0 to add, 0 to change, 4 to destroy.
    
    Do you really want to destroy all resources?
      Terraform will destroy all your managed infrastructure, as shown above.
      There is no undo. Only 'yes' will be accepted to confirm.
    
      Enter a value: yes
    
    yandex_compute_instance.default: Destroying... [id=fhmpldmndpo4ufoji6gf]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 10s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 20s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 30s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 40s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 50s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 1m0s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 1m10s elapsed]
    yandex_compute_instance.default: Still destroying... [id=fhmpldmndpo4ufoji6gf, 1m20s elapsed]
    yandex_compute_instance.default: Destruction complete after 1m30s
    yandex_vpc_subnet.default: Destroying... [id=e9bc80kd45lfmfq2fq0d]
    yandex_compute_disk.default: Destroying... [id=fhm3acu0uitbelemhm0k]
    yandex_compute_disk.default: Destruction complete after 0s
    yandex_vpc_subnet.default: Destruction complete after 5s
    yandex_vpc_network.default: Destroying... [id=enpvpoj117va949tjmae]
    yandex_vpc_network.default: Destruction complete after 0s
    
    Destroy complete! Resources: 4 destroyed.
    

## Собирая все вместе
    
    
    # gitignore
    .terraform
    *.auto.tfvars
    *.backup
    
    
    
    // main.tf
    terraform {
      required_providers {
        yandex = {
          source = "yandex-cloud/yandex"
        }
      }
      required_version = ">= 0.13"
    }
    
    variable "yc_token" {}
    
    provider "yandex" {
      zone = "ru-central1-a"
      token = var.yc_token
    }
    
    resource "yandex_compute_instance" "default" {
      name        = "test"
      platform_id = "standard-v1"
      zone        = "ru-central1-a"
      folder_id   = "<идентификатор каталога>"
    
      resources {
        cores  = 2
        memory = 4
      }
    
      boot_disk {
        disk_id = yandex_compute_disk.default.id
      }
    
      network_interface {
        subnet_id = "${yandex_vpc_subnet.default.id}"
      }
    
      metadata = {
        ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
      }
    }
    
    resource "yandex_vpc_network" "default" {
      folder_id = "<идентификатор каталога>"
    }
    
    resource "yandex_vpc_subnet" "default" {
      zone           = "ru-central1-a"
      network_id     = "${yandex_vpc_network.default.id}"
      v4_cidr_blocks = ["10.5.0.0/24"]
      folder_id      = "<идентификатор каталога>"
    }
    
    resource "yandex_compute_disk" "default" {
      name     = "disk-name"
      type     = "network-ssd"
      zone     = "ru-central1-a"
      image_id = "fd83s8u085j3mq231ago"
      folder_id = "<идентификатор каталога>"
    
      labels = {
        environment = "test"
      }
    }
    
    
    
    // secrets.auto.tfvars
    yc_token = "<api key>"
    

* * *

#### Самостоятельная работа

Выполните все действия из теории к уроку

* * *

#### Дополнительные материалы

  1. Terraform Example (Github)
  2. Автоматическое форматирование конфигурации
