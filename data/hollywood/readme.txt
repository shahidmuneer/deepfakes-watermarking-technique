
HOLLYWOOD HUMAN ACTIONS (HOHA)
==============================================================================

This archive provides the video samples and annotations used in the
experimental section of the paper "Learning realistic human actions
from movies" by I. Laptev, M. Marszalek, C. Schmid and B. Rozenfeld,
published in CVPR 2008.


ARCHIVE CONTENT
------------------------------------------------------------------------------

The archive contains the following two directories:


./videoclips/

The directory contains video clips, i.e., short sequences from 32 movies:
American Beauty, As Good As It Gets, Being John Malkovich, Big Fish, The Big
Lebowski, Bringing Out The Dead, The Butterfly Effect, Casablanca, The Crying
Game, Dead Poets Society, Double Indemnity, Erin Brockovich, Fargo, Forrest
Gump, Gandhi, The Godfather, The Graduate, I Am Sam, Independence Day, Indiana
Jones And The Last Crusade, Its A Wonderful Life, Kids, LA Confidential,
LOR - Fellowship Of The Ring, Lost Highway, The Lost Weekend, Mission To Mars,
The Naked City, The Pianist, Pulp Fiction, Raising Arizona, Reservoir Dogs.

The video frames typically consist of 240 lines, the aspect ratios vary.
The videos run at about 24 fps. The clips are encoded using the DivX 5 codec,
see http://www.divx.com/


./annotations/

The content of the directory defines video samples as fragments of the
video clips. The fragments are specified by frame ranges. For the automatic
training, samples correspond to full clips. For manual annotations, clips
could be trimmed or split. Each sample is annotated according to 8 classes:
AnswerPhone, GetOutCar, HandShake, HugPerson, Kiss, SitDown, SitUp, StandUp.

For each sample an annotation of the following format is provided:

"filename.avi" (start_frame-end_frame) <action_label1> [<action_label2> [...]]

The filenames may contain spaces or punctuation, the first frame in each clip
has an index of 1, the frame ranges are inclusive and a sample may feature
more than one action.

For our experiments we used two training sets and one test set. The training
and test sets originate from separate sets of movies. The three subsets of
samples are defined in the following files:


./annotations/train_auto.txt

This subset of samples originates from 12 movies. Its samples correspond to
the results of automatic clip retrieval and annotation based on movie scripts.
It consists of 233 action samples with 239 automatically assigned labels of
which 143 are correct. The incorrect labels do not correspond to the visual
content due to errors in the automatic annotation. We used this subset for
training to evaluate the robustness of our method to training noise and to
demonstrate the automatic visual training of an action classifier.


./annotations/train_clean.txt

This subset originates from the same 12 movies as the automatic one. It
contains 219 action samples that were manually verified to have 231 correct
labels. In addition to the 143 samples from the automatic set, this subset
has samples obtained via manual video annotation. The temporal extents for
long episodes were manually cropped with respect to a rough action time
interval. We used this subset to train an action classifier in a "clean"
setting with correctly labeled training data.


./annotations/test_clean.txt

This subset originates from 20 movies, different from the movies of the
training set. It consists of 211 manually annotated action samples with
217 labels. We used this set for testing our action recognition system
after training with either automatic or clean training subsets.


REFERENCES
------------------------------------------------------------------------------

To cite this database please use:

@InProceedings{laptev:08,
  author       = "Ivan Laptev and Marcin Marsza{\l}ek and Cordelia Schmid and Benjamin Rozenfeld",
  title        = "Learning Realistic Human Actions from Movies",
  booktitle    = "IEEE Conference on Computer Vision \& Pattern Recognition",
  year         = "2008"
}
