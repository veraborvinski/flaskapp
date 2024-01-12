variable "machine_name" {
  type        = string
  description = "The machine name"
  default     = "myflix2"
}

variable "project" {
  type        = string
  description = "The project ID to deploy to"
  default     = "kinetic-dryad-405523"
}

variable "region" {
  type        = string
  description = "The region to deploy to"
  default     = "europe-west2"

}

variable "zone" {
  type        = string
  description = "The zone to deploy to"
  default     = "europe-west2-c"
}
