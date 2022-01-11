# set display to control
export DISPLAY=:0

# portrait screen (right)
xrandr -o right

# portrait touch (right)
xinput set-prop "ILITEK Multi-Touch-V5000" --type=float "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1

# run chrome
google-chrome --kiosk https://mapt-1b9b0.web.app/Home


