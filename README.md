# MotionCanvasArtistry

-- --
## Installing Dependencies
`pip install -r requirements.txt`
-- --

## Running
`python main.py [arg1] [arg2] [arg3] [arg4] [arg5] [arg6] [arg7] [arg8] [arg9]`

#### Args:

`[arg1]` - `device_id` (Determines which device to use as a live camera) `Example: 0`

`[arg2]` - `factor` (Determines how many pixels should be covered by 1 sphere) `Example: 10`

`[arg3]` - `width` (Determines output window width) `Example: 480`

`[arg4]` - `height` (Determines output window height) `Example: 480`

`[arg5]` - `black_depth` (Determines the lowest level of black color in range [0, 255]. Under this level the color will be ignored and sphere will not be created for this pixel) `Example: 16 (If you do not want to ignore any pixels use -1)`

`[arg6]` - `speed` (Determines the movement speed of the spheres) `Example: 2`

`[arg7]` - `spawn_range` (Determines how many spheres should be spawn at once when if count of the spheres become lower than the minimum quantity acceptable) `Example: 3`

`[arg8]` - `grow_speed` (Determines the growth speed of the sphere radius) `Example: 2`

`[arg9]` - `image_path` (Determines starting image path [ONLY THE NAME of the image should be plugged. The image should be stored in 'mock_data/images'] and be in '.JPG' format) `Example: mock5`

-- --

## Comment
Use `SQUARE` images only. `Width AND height` of the image must be equal to the `HEIGHT` of the live camera resolution.

-- --