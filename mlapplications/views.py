from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
# import torch
from articles.models import Article, Reviewer_publication
from profiles.models import Profiles
# from transformers import AutoModel, AutoTokenizer
import numpy as np
import pandas as pd
from joblib import load
from xgboost import XGBRegressor
import re
import datetime
# from sentence_transformers import SentenceTransformer, util
from django.contrib.auth.decorators import user_passes_test, login_required
from profiles.views import is_editor, is_reviewer, is_editor_or_reviewer

# # model_name = "model/arabert"
# model_name = "aubmindlab/bert-base-arabertv2"

# arabert_model = AutoModel.from_pretrained(model_name, return_dict=True)
# tokenizer = AutoTokenizer.from_pretrained(model_name)


# target_list =['	إقتصاد زراعي',	'	تقانات حيوية',	'محاصيل حقلية',
#               'بيئة',	'تكنولوجيا الأغذية',	'بستنة',	'إنتاج حيواني',
#               'موارد طبيعية',	'	وقاية النبات']
# # target_list =['Agricultural_Economics',	'Agriculture_Biotechnology',	'Crop_production',
# #               'Environmental_Sciences',	'Food_Technology',	'Horticulture',	'Livestock_production',
# #               'Natural_Resources',	'Plant_Protection']
# MAX_LEN = 256
# device = torch.device('cpu')

# class BERTClass(torch.nn.Module):
#     def __init__(self):
#         super(BERTClass, self).__init__()
#         self.model = arabert_model
#         self.dropout = torch.nn.Dropout(0.3)
#         self.linear = torch.nn.Linear(768, 9)

#     def forward(self, input_ids, attn_mask, token_type_ids):
#         output = self.model(
#             input_ids,
#             attention_mask=attn_mask,
#             token_type_ids=token_type_ids
#         )
#         output_dropout = self.dropout(output.pooler_output)
#         output = self.linear(output_dropout)
#         return output

# bert_model = BERTClass()
# bert_model.load_state_dict(torch.load('model/arabert_classifier.pt', map_location=device))
# bert_model.eval()

def arabert_predict(request, article_id):
#   reviewed_article = get_object_or_404(Article, id=article_id)

#   sample = reviewed_article.title + reviewed_article.abstract
# #   sample = request.GET('sample')
#   encodings = tokenizer.encode_plus(
#     sample,
#     None,
#     add_special_tokens=True,
#     max_length= 256,
#     padding='max_length',
#     return_token_type_ids=True,
#     truncation=True,
#     return_attention_mask=True,
#     return_tensors='pt'
#   )
#   bert_model.eval()
#   with torch.no_grad():
#     input_ids = encodings['input_ids'].to(device, dtype=torch.long)
#     attention_mask = encodings['attention_mask'].to(device, dtype=torch.long)
#     token_type_ids = encodings['token_type_ids'].to(device, dtype=torch.long)
#     output = bert_model(input_ids, attention_mask, token_type_ids)
#     final_output = torch.sigmoid(output).cpu().detach().numpy().tolist()
#     # print(train_dataset.columns[1:].to_list()[(np.argmax(final_output, axis=1)).astype(int)])
#     predictions = []
#     for idx, label in enumerate(target_list):
#       if (final_output[0][idx] > 0.5):
#         predictions.append((label,round(final_output[0][idx]*100, 2)))  # round(preds[idx]*100, 2
#     context = {'predictions' : predictions, 'final_output': final_output}
    return render(request, 'mlapplications/scope_predictions.html')#, context)


@login_required
@user_passes_test(is_editor)
def decision_prediction(request, article_id):
  reviewed_article = get_object_or_404(Article, id=article_id)
  full_text = reviewed_article.title + reviewed_article.abstract \
    + reviewed_article.introduction + reviewed_article.key_words \
    + reviewed_article.en_keyword + reviewed_article.en_abstract + reviewed_article.references
  fitted_vectorizer = load("model/tfidf.pkl")
  lgbm_model = load("model/decision_lgbm.pkl")
  transformed_text = fitted_vectorizer.transform([full_text])
  predicted = lgbm_model.predict(transformed_text)

  context = {
            'result': round(predicted[0], 2),
            'full_text': full_text}
  return render(request, 'mlapplications/decision_predictions.html', context)


def get_latest_reference_year(references):
  pattern = re.compile(r'\d\d\d\d')
  references_years = pattern.findall(references)
  today = datetime.date.today()
  years = [int(y) for y in references_years if (int(y) > (today.year - 70) and int(y)< today.year)]
  if (len(years) > 0 ):
    return (len(years), max(years), min(years), round(np.mean(years),2), round(np.median(years),2))
  else:
    print('empty')
    return (0, 0, 0, 0, 0)

# number of figurs & tabels
def get_figurs(paper_txt):
  pattern1 = re.compile(r'شكل') # *\s*.\d')
  pattern2 = re.compile(r'شكل*\sرقم*.\d')
  pattern3 = re.compile(r'جدول') # *\s*.\d')  # *.\d
  pattern4 = re.compile(r'جدول*\sرقم*.\d')
  pattern5 = re.compile(r'مخطط*\s*.\d')
  pattern6 = re.compile(r'مخطط*\sرقم*.\d')


  figurs = pattern1.findall(paper_txt)
  figurs2 = pattern2.findall(paper_txt)
  tabels = pattern3.findall(paper_txt)
  tabels2 = pattern4.findall(paper_txt)
  charts = pattern5.findall(paper_txt)
  charts2 = pattern6.findall(paper_txt)

  join = lambda x: ' '.join(x)
  figurs = join(figurs) + join(figurs2)
  tabels = join(tabels) + join(tabels2)
  charts = join(charts) + join(charts2)

  pattern4 = re.compile(r'\d')
  fig_num = pattern4.findall(figurs)
  tab_num = pattern4.findall(tabels)
  chr_num = pattern4.findall(charts)

  if len(fig_num)>0: max_fig = int(max(fig_num))
  else: max_fig = 0
  if len(tab_num)>0: max_tab = int(max(tab_num))
  else: max_tab = 0
  if len(chr_num)>0: max_chrt = int(max(chr_num))
  else: max_chrt = 0

  return (max_fig, max_tab, max_chrt)

def avg_recent_ref(latest,oldest,median):
  a = latest - median
  b = latest - oldest
  if b > 0:
    return (a/b)
  else: return 0

# english/arabic words average
def ar_counter(text):
    ar_text = re.findall(r'[\u0600-\u06ff]+', str(text))
    return len(ar_text)

def en_counter(text):
  en_text = re.findall(r"[a-z]['\w]*", str(text))
  return len(en_text)

def num_sentence(paper):
  sentences = paper.split('.')
  counter = 0
  for sent in sentences:
    if (len(sent.split()) >3):
      counter += 1
  return counter

def avg_words_per_sent(paper):
  sentences = paper.split('.')
  counter = 0
  len_list = 0
  for sent in sentences:
    if (len(sent.split()) >3):
      counter += 1
      len_list += (len(sent.split()))
  if counter > 0:
    return (len_list / counter)
  else:
    return 0

def ref_mention_counts(paper, oldest_ref, latest_ref):
  count = 0
  for ref in range(oldest_ref, latest_ref+1):
    count += paper.count(str(ref))
  return count


from django.http import HttpResponse
from django.template import Context, Template


@login_required
@user_passes_test(is_editor)
def quality_prediction(request, article_id):

  reviewed_article = get_object_or_404(Article, id=article_id)
  references = reviewed_article.references
  paper_txt = reviewed_article.introduction
  full_txt = reviewed_article.title + reviewed_article.abstract + reviewed_article.key_words + reviewed_article.en_abstract + reviewed_article.en_keyword + paper_txt + references
  data = []
  num_references , latest_reference, oldest_reference, me, meadian_reference = get_latest_reference_year(references)
  if num_references < 5:
    context = {'result': "can't make predictions, no references found!"}
    return render(request, 'mlapplications/quality_predictions.html', context)

  
  num_figurs, num_tables, num_charts = get_figurs(paper_txt)
  num_authors = reviewed_article.author.count()
  avg_recent_references = avg_recent_ref(latest_reference,oldest_reference,meadian_reference)
  paper_len = len(full_txt.split())
  ar_word_count = ar_counter(full_txt)
  en_word_count = en_counter(full_txt)
  if paper_len > 50 :
    ar_word_avg = float(ar_word_count)/float(paper_len)
    en_word_avg = float(en_word_count)/float(paper_len)
  else:
      context = {'result': "can't make predictions, article is too short!"}
      return render(request, 'mlapplications/quality_predictions.html', context)

  num_sentences = num_sentence(full_txt)
  avg_words_per_sentence = avg_words_per_sent(full_txt)
  ref_mention_count = ref_mention_counts(full_txt, oldest_reference, latest_reference)

  counts_list = []
  al =  reviewed_article.author.values_list('id')
  for auth in reviewed_article.author.values_list('id'):
    aut = User.objects.get(id=auth[0])
    count2 = aut.profiles.publications_count
    if count2:
      counts_list.append(count2)

  if len(counts_list) > 0 :  num_publication = max(counts_list)
  else: num_publication = 0

  data.append(num_references)
  data.append(latest_reference)
  data.append(oldest_reference)
  data.append(meadian_reference)
  data.append(num_figurs)
  data.append(num_tables)
  data.append(num_charts)
  data.append(num_authors)
  data.append(avg_recent_references)
  data.append(paper_len)
  data.append(ar_word_count)
  data.append(en_word_count)
  data.append(ar_word_avg)
  data.append(en_word_avg)
  data.append(num_sentences)
  data.append(avg_words_per_sentence)
  data.append(ref_mention_count)
  data.append(num_publication)

  stat_labels = ['num_references', 'latest_reference', 'oldest_reference',
        'meadian_reference', 'num_figurs', 'num_tables', 'num_charts',
        'num_authors', 'avg_recent_references', 'paper_len', 'ar_word_count',
        'en_word_count', 'ar_word_avg', 'en_word_avg', 'num_sentences',
        'avg_words_per_sentence', 'ref_mention_count', 'num_publication']
  cdata = np.array(data)
  df = pd.DataFrame(cdata.reshape(1,-1), columns=stat_labels)
  xgbr_model = XGBRegressor()
  xgbr_model.load_model('model/quality_xgbm_regression_model.json')
  result = xgbr_model.predict(df)
  # cc = request.GET.get('quality')
  # cc = result
  context = {'result': round(result[0], 2)}
  # template = Template(str(round(result[0], 2)))
  # context = Context(con)

  # result = template.render(context)
  # return HttpResponse(result)
  # return TemplateResponse(request, 'articles/article_review.html', context)
  return render(request, 'mlapplications/quality_predictions.html', context)
  # return redirect('article-review', article_id= article_id)



# embedder = SentenceTransformer(model_name)
@login_required
@user_passes_test(is_editor)
def reviewer_recommender(request, article_id):

  # # get authors list for this article
  # reviewed_article = get_object_or_404(Article, id=article_id)
  # authors = reviewed_article.author.values_list('id')
  # authors_list = []
  # for a in authors:
  #   authors_list.append(a)

  # # get topic list for this article
  # publications = []
  # paper_scope = reviewed_article.scope.values_list('id')
  # paper_scope_list = []
  # for r in paper_scope:
  #   paper_scope_list.append(r[0])
  #   publication_scope = Reviewer_publication.objects.filter(scope = r[0]).values_list('user_id')
  #   target_publications = [pub for pub in publication_scope if pub not in authors_list]

  #   targets = []
  #   for target in target_publications:
  #     current_user = Profiles.objects.get(id=target[0])
  #     if current_user.user_type == 'REVIEWER':
  #       targets.append(target)

  #   for p in targets:
  #     publications.append(p[0])
  
  # # removing duplicated values:
  # list_set = set(publications)
  # publications = list(list_set)

  # # embedding query string:
  # query_embedding = embedder.encode(reviewed_article.abstract, convert_to_tensor=True)
  # results =[]
  # ids =[]
  # for u_id in publications:
  #   abstract = Reviewer_publication.objects.filter(user_id = u_id).values_list('abstract')
  #   art_emp = embedder.encode(abstract[0], convert_to_tensor=True, show_progress_bar=True)
  #   # cosin similarity between query string & each publication
  #   res = util.cos_sim(query_embedding, art_emp).item()
  #   results.append(res)
  #   ids.append(u_id)
  # top_simi = sorted(zip(results, ids), reverse=True)

  # output = []
  # scope_output = []
  # similarity_value = []
  # reviewer_name = []
  # reviewer_specialist = []
  # reviewer_specific_specialist = []
  # final = []
  # topn = min(len(publications), 10) #topN)
  # for i in range(topn):
  #   related_paper = Reviewer_publication.objects.get(user_id =top_simi[i][1])
  #   scope_output.append(related_paper.scope.values_list('scope'))
  #   output.append(related_paper.abstract)
  #   reviewer = Profiles.objects.get(id =top_simi[i][1])
  #   reviewer_name.append(reviewer.name)
  #   reviewer_specialist.append(reviewer.specialist)
  #   reviewer_specific_specialist.append(reviewer.specific_specialist)
  #   result = {'similarity_value': round(top_simi[i][0],2),
  #          'reviewer_id': reviewer.id,
  #          'reviewer_name': reviewer.name,
  #          'reviewer_specialist': reviewer.specialist,
  #          'reviewer_specific_specialist': reviewer.specific_specialist,
  #          'abstract': related_paper.abstract,
  #          'scope_output': related_paper.scope.values_list('scope')}
  #   final.append(result)
  #   similarity_value.append(top_simi[i][0])

  # context = {'reviewed_article': reviewed_article,
  #            'final': final,
  #           }
  return render(request, 'mlapplications/reviewer_recommender.html')#, context)

@login_required
@user_passes_test(is_editor)
def extra_reviewer_recommender(request, article_id):
  # # get authors list for this article
  # reviewed_article = get_object_or_404(Article, id=article_id)
  # authors = reviewed_article.author.values_list('id')
  # authors_list = []
  # for a in authors:
  #   authors_list.append(a[0])

  # # get topic list for this article
  # # publications = []
  # ids_list = []
  # paper_scope = reviewed_article.scope.values_list('id')
  # paper_scope_list = []
  # for r in paper_scope:
  #   paper_scope_list.append(r[0])
  #   publication_scope = Article.objects.filter(scope = r[0]).values_list('author')
  #   for i in publication_scope:
  #     # for p in paper.values_list('id'):
  #     if i[0] not in authors_list:
  #       ids_list.append(i[0])

  
  # # removing duplicated values:
  # list_set = set(ids_list)
  # ids_list = list(list_set)

  # certificated_reviewer = []
  # certificated = Profiles.objects.filter(id__in = ids_list).filter(certificate__in = ['الدكتور', 'الدكتورة'])
  # for cert in certificated:
  #   if cert.pk not in authors_list:
  #     certificated_reviewer.append(cert.pk)

  # # embedding query string:
  # query_embedding = embedder.encode(reviewed_article.abstract, convert_to_tensor=True)
  # results =[]
  # rev_ids =[]
  # art_ids =[]
  # for u_id in certificated_reviewer:
  #   article = Article.objects.filter(author = u_id).filter(scope__in = paper_scope_list)
  #   for art in article:
  #     if art.pk not in art_ids:
  #       abstract = art.abstract
  #       if (abstract and len(abstract) > 10):
  #         art_emp = embedder.encode(abstract, convert_to_tensor=True, show_progress_bar=True)
  #         # cosin similarity between query string & each publication
  #         res = util.cos_sim(query_embedding, art_emp).item()
  #         results.append(res)
  #         rev_ids.append(u_id)
  #         art_ids.append(art.pk)
  # top_simi = sorted(zip(results, rev_ids, art_ids), reverse=True)
  # output = []
  # scope_output = []
  # similarity_value = []
  # reviewer_name = []
  # reviewer_specialist = []
  # reviewer_specific_specialist = []
  # final = []
  # topn = min(len(certificated_reviewer), 10) #topN)
  # for i in range(topn):
  #   related_paper = Article.objects.get(id =top_simi[i][2])
  #   scope_output.append(related_paper.scope.values_list('scope'))
  #   output.append(related_paper.abstract)
  #   reviewer = Profiles.objects.get(id =top_simi[i][1])
  #   reviewer_name.append(reviewer.name)
  #   reviewer_specialist.append(reviewer.specialist)
  #   reviewer_specific_specialist.append(reviewer.specific_specialist)
  #   result = {'similarity_value': round(top_simi[i][0],2),
  #          'reviewer_id': reviewer.id,
  #          'reviewer_name': reviewer.name,
  #          'reviewer_specialist': reviewer.specialist,
  #          'reviewer_specific_specialist': reviewer.specific_specialist,
  #          'abstract': related_paper.abstract,
  #          'scope_output': related_paper.scope.values_list('scope')}
  #   final.append(result)
  #   similarity_value.append(top_simi[i][0])

  # context = {'ids_list': ids_list,
  #            'certificated_reviewer': certificated_reviewer,
  #            'len_ids_list': len(ids_list),
  #            'len_certificated_reviewer': len(certificated_reviewer),
  #            'reviewer_name': reviewer_name,
  #            'result': final,
  #            'authors_list': authors_list,
  #            'paper_scope_list': paper_scope_list,
  #            'reviewed_article': reviewed_article,
  #           }
  return render(request, 'mlapplications/reviewer_recommender_plus.html')#, context)
