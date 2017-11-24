#!/bin/bash
( cd Users_MS && docker build -t jaimelive/users_ms . )
( cd Main_App && docker build -t jaimelive/main_app . )

