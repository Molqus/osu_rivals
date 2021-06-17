# osu_rivals

comparing your score and rival score. only available in osu!catch now.

## Notice

I'll transfer the ownership of this repository to my main account because I realized I'm not allowed to make alt acccount in github.

## Usage

using [poetry](https://python-poetry.org/) to manage modules.

```
poetry install
```

you can also use pip to install dependencies:

```
pip install -r requirements.txt
```

to run under local environment, you should put `osu/API_KEY` file with your osu api written on it. you can get api key from [here](https://osu.ppy.sh/p/api/) (required osu account).
and you need to run `osu/data.py` to get ranked beatmap data (it'll be saved as `data/beatmaps.json`) and get all score (it'll be saved to postgresql), but I'm now fixing(rewriting) this file because I wrote this file assuming that using sqlite.
to get beatmap data, you should run:

```
python3 osu/data.py -gb
```

and then start to collect. if the process stopped suddenly (because of server issue or etc), you can use this command to continue:

```
python3 osu/data.py -ub
```
